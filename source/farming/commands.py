import datetime
import os as fs
import time
import webbrowser
import subprocess
from datetime import datetime
from random import randint
import json

import api.auth as auth
import api.caches as caches
import api.ingame as ingame
import api.outgame as outgame
import api.transfer as transfer
import config as config
import farming.facebook as facebook
import farming.fapro as farmbot
import utils.colors as colors
import utils.crypto as crypto
import utils.database as database
import utils.error as error
import utils.funcs as funcs
from colorama import init, Fore

init(autoreset=True)

farm = []


def handler(msg):
    global farm
    args = msg.split(' ')
    # ===== base =====
    # new
    if args[0].lower() == 'new' and caches.loaded is None:
        if len(args) == 3 and '' not in args:
            if args[1] == 'gb' and not config.gb_maint or args[1] == 'jp' and not config.jp_maint:
                if args[2] == 'ios' or args[2] == 'android':
                    store = auth.register(args[1], args[2])
                    if 'error' not in store[0]:
                        if 'captcha_url' in store[0]:
                            url = store[0]['captcha_url']
                            key = store[0]['captcha_session_key']
                            webbrowser.open(url, new=1, autoraise=True)
                            print(colors.render('{message}Complete CAPTCHA to continue... Press ENTER when done.'))
                            input()
                            store = auth.register(args[1], args[2], store[1], store[2], key)
                            if 'error' not in store[0]:
                                if 'identifier' in store[0]:
                                    store2 = auth.login(args[1], args[2], crypto.basic(store[0]['identifier']), True)
                                    if 'error' not in store2:
                                        farmbot.tutorial(args[1], args[2], store2['access_token'], store2['secret'],
                                                         store[0]['identifier'])
                                        farmbot.gifts()
                                        farmbot.missions()
                                        print(colors.render('{message}type "help" for a list of commands.'))
                                    else:
                                        error.handler('new login', store2)
                                else:
                                    error.handler('register2', store[0])
                            else:
                                error.handler('register2', store[0])
                        else:
                            error.handler('register111', store)
                    else:
                        error.handler('register1', store[0])
                else:
                    print(colors.render('{error}invalid OS input.'))
            else:
                if args[1] == 'gb' and config.gb_maint or args[1] == 'jp' and config.jp_maint:
                    print(colors.render('{error}[' + str(args[1]).upper() + '] servers are under maintenance!'))
                else:
                    print(colors.render('{error}invalid version input.'))
        else:
            print(colors.render('{error}new gb/jp ios/android'))
        return 1
    # reroll
    if args[0].lower() == 'reroll' and caches.loaded is None:
        if len(args) >= 3 and '' not in args:
            if args[1] == 'gb' and not config.gb_maint or args[1] == 'jp' and not config.jp_maint:
                if args[2] == 'ios' or args[2] == 'android':
                    if len(args) == 4:
                        if int(args[3]) <= config.max_mass_rerolls:
                            for i in range(int(args[3])):
                                ver, os = args[1], args[2]
                                subprocess.run('start cmd.exe /k python bot.pyc reroll start ' + ver + ' ' + os,
                                               shell=True, check=False)
                            exit()
                        else:
                            print(colors.render('{error}your choice of ' + str(
                                args[3]) + ' rerolls is too many.\nthe limit is ' + str(
                                config.max_mass_rerolls) + ' or less to prevent system failure.'))
                    else:
                        store = auth.register(args[1], args[2])
                        if 'error' not in store:
                            url = store[0]['captcha_url']
                            key = store[0]['captcha_session_key']
                            webbrowser.open(url, new=1, autoraise=True)
                            print(colors.render('{message}Complete CAPTCHA to continue... Press ENTER when done.'))
                            input()
                            store = auth.register(args[1], args[2], store[1], store[2], key)
                            if 'error' not in store:
                                store2 = auth.login(args[1], args[2], crypto.basic(store[0]['identifier']), True)
                                if 'error' not in store2:
                                    farmbot.tutorial(args[1], args[2], store2['access_token'], store2['secret'],
                                                     store[0]['identifier'])
                                    farmbot.gifts()
                                    farmbot.missions()
                                    farmbot.streamline('quests')
                                    funcs.refresh()
                                    farmbot.streamline('events')
                                    funcs.refresh()
                                    farmbot.streamline('ezas')
                                    funcs.refresh()
                                    farmbot.gifts()
                                    farmbot.missions()
                                else:
                                    error.handler('nw login', store2)
                            else:
                                error.handler('rgister2', store)
                        else:
                            error.handler('rgister1', store)
                else:
                    print(colors.render('{error}invalid OS input.'))
            else:
                if args[1] == 'gb' and config.gb_maint or args[1] == 'jp' and config.jp_maint:
                    print(colors.render('{error}[' + str(args[1]).upper() + '] servers are under maintenance!'))
                else:
                    print(colors.render('{error}invalid version input.'))
        else:
            print(colors.render('{error}reroll gb/jp ios/android'))
        return 1
    # transfer
    if args[0].lower() == 'add' and caches.loaded is None:
        iden = None
        try:
            if len(args) == 3:
                if args[1] == 'gb' and not config.gb_maint or args[1] == 'jp' and not config.jp_maint:
                    acc_ver = args[1]
                    tc = args[2]
                    fc = '000000000'
                    store = transfer.validate(acc_ver, tc, fc)
                    if 'error' not in store:
                        if not store['platform_difference']:
                            acc_os = 'android'
                        else:
                            acc_os = 'ios'
                        store = transfer.use(acc_ver, acc_os, tc, fc)
                        if 'error' not in store:
                            iden = store['identifiers'].replace('\n', '')
                            print(Fore.YELLOW + 'identifier for recover.\n' + iden)
                            store = auth.login(acc_ver, acc_os, crypto.basic(iden), False)
                            if 'error' not in store:
                                if 'reason' not in store:
                                    save = funcs.create_save_file(acc_ver, acc_os, iden)
                                    caches.load_account(save, iden, acc_ver, acc_os, store['access_token'], store['secret'], True)
                                    # funcs.help2()
                                else:
                                    url = store['captcha_url']
                                    key = store['captcha_session_key']
                                    webbrowser.open(url, new=1, autoraise=True)
                                    print(colors.render('{message}Complete CAPTCHA to login... Press ENTER when done.'))
                                    input()
                                    store = auth.login(acc_ver, acc_os, crypto.basic(iden), False, key)
                                    if 'error' not in store:
                                        save = funcs.create_save_file(acc_ver, acc_os, iden)
                                        caches.load_account(save, iden, acc_ver, acc_os, store['access_token'], store['secret'], True)
                                        # funcs.help2()
                                    else:
                                        error.handler('add login2', store)
                            else:
                                error.handler('add login', store)
                        else:
                            error.handler('add use', store)
                    else:
                        error.handler('add validate', store)
                else:
                    if args[1] == 'gb' and config.gb_maint or args[1] == 'jp' and config.jp_maint:
                        print(colors.render('{error}[' + str(args[1]).upper() + '] servers are under maintenance!'))
                    else:
                        print(colors.render('{error}invalid version input.'))
            else:
                print(colors.render('{error}add gb/jp TC'))
        except:
            print(colors.render(
                '{error}Something went wrong... use your identifier to recover.\n' + Fore.LIGHTYELLOW_EX + iden))
        return 0
    # link
    if args[0].lower() == 'link' and caches.loaded is None:
        if len(args) == 3 and '' not in args:
            if args[1] == 'gb' and not config.gb_maint or args[1] == 'jp' and not config.jp_maint:
                if args[2] == 'ios' or args[2] == 'android':
                    url = facebook.loginPage(args[1])
                    facebook.webView(args[1], args[2], url, 1)
                else:
                    print(colors.render('{error}invalid OS input.'))
            else:
                if args[1] == 'gb' and config.gb_maint or args[1] == 'jp' and config.jp_maint:
                    print(colors.render('{error}[' + str(args[1]).upper() + '] servers are under maintenance!'))
                else:
                    print(colors.render('{error}invalid version input.'))
        else:
            print(colors.render('{error}link gb/jp ios/android'))
        return 1
    # load
    if args[0].lower() == 'load' and caches.loaded is None:
        if len(args) == 2 and '' not in args:
            save = args[1].lower()
            if fs.path.isfile('../saves/' + save + '.txt'):
                f = open('../saves/' + save + '.txt', 'r')
                line1 = f.readline().rstrip().split(':')
                acc_ver = line1[0]
                acc_os = line1[1]
                iden = f.readline().rstrip()
                f.close()
                if acc_ver == 'gb' and not config.gb_maint or acc_ver == 'jp' and not config.jp_maint:
                    store = auth.login(acc_ver, acc_os, crypto.basic(iden), False)
                    #print(store)
                    if 'error' not in store:
                        if 'reason' not in store:
                            caches.load_account(save, iden, acc_ver, acc_os, store['access_token'], store['secret'], True)
                        else:
                            url = store['captcha_url']
                            key = store['captcha_session_key']
                            webbrowser.open(url, new=1, autoraise=True)
                            print(colors.render('{message}Complete CAPTCHA to login... Press ENTER when done.'))
                            input()
                            store = auth.login(acc_ver, acc_os, crypto.basic(iden), False, key)
                            if 'error' not in store:
                                caches.load_account(save, iden, acc_ver, acc_os, store['access_token'], store['secret'], True)
                            else:
                                error.handler('load capt', store)
                    else:
                        error.handler('load login', store)
                else:
                    print(colors.render('{error}[' + str(acc_ver).upper() + '] servers are under maintenance!'))
            else:
                print(colors.render('{error}that save doesn\'t exist.'))
        else:
            print(colors.render('{error}you didn\'t select a save.'))
        return 1
    # daily
    if args[0].lower() == 'daily' and caches.loaded is None:
        for i in fs.listdir('../saves'):
            save_file = open('../saves/' + str(i), 'r')
            txt = save_file.read().split('\n')
            ver, os, save, iden = txt[0].split(':')[0], txt[0].split(':')[1], str(i), txt[1]
            save_file.close()
            if ver == 'gb' and not config.gb_maint or ver == 'jp' and not config.jp_maint:
                try:
                    store = auth.login(ver, os, crypto.basic(iden), False)
                    if 'error' not in store:
                        if 'reason' not in store:
                            caches.load_account(save, iden, ver, os, store['access_token'], store['secret'])
                            store = caches.events
                            for e in store['events']:
                                if int(e['id']) == 111 or int(e['id']) == 116 or int(e['id']) == 120 or int(
                                        e['id']) == 130 or int(e['id']) == 131 or int(e['id']) == 132 or int(
                                    e['id']) == 134 or int(e['id']) == 135 or int(e['id']) == 177:
                                    if 'quests' in e:
                                        for x in e['quests']:
                                            for j in database.fetchAll(ver + '.db', 'sugoroku_maps',
                                                                       'quest_id=' + str(x['id'])):
                                                farmbot.handler(0, x['id'], j[2])
                        else:
                            url = store['captcha_url']
                            key = store['captcha_session_key']
                            webbrowser.open(url, new=1, autoraise=True)
                            print(colors.render('{message}Complete CAPTCHA to login... Press ENTER when done.'))
                            input()
                            store = auth.login(ver, os, crypto.basic(iden), False, key)
                            if 'error' not in store:
                                caches.load_account(save, iden, ver, os, store['access_token'], store['secret'])
                                store = caches.events
                                for e in store['events']:
                                    if int(e['id']) == 111 or int(e['id']) == 116 or int(e['id']) == 120 or int(
                                            e['id']) == 130 or int(e['id']) == 131 or int(e['id']) == 132 or int(
                                        e['id']) == 134 or int(e['id']) == 135 or int(e['id']) == 177:
                                        if 'quests' in e:
                                            for x in e['quests']:
                                                for j in database.fetchAll(ver + '.db', 'sugoroku_maps',
                                                                           'quest_id=' + str(x['id'])):
                                                    farmbot.handler(0, x['id'], j[2])
                            else:
                                error.handler('dailycapt', store)
                        farmbot.missions()
                        farmbot.gifts()
                    else:
                        print('Error with: ' + str(i))
                        error.handler('daily(s)', store)
                except:
                    print('Error with: ' + str(i) + '\nCannot use this identifier!')
            else:
                print(colors.render('{error}[' + str(ver).upper() + '] servers are under maintenance!'))
        print(colors.render('{success}daily farm on all saves complete.'))
        caches.loaded = None
        return 0
    # summary
    if args[0].lower() == 'summary' and caches.loaded is None:
        date = str(int(time.time()))
        f = open('../summaries/' + date + '.html', 'w')
        f.write(
            '<html><body><style>h1{text-align:center;}table{width:100%;border:0}th{'
            'font-size:15px;background-color:gray;border-width:1px;padding:8px;border-style:solid;border-color:black'
            ';text-align:left;}td{border-width:1px;padding:8px;border-style:solid;border-color:black;}</style><h1'
            '>Android 16 - Summary</h1><table><tr><th>Save, Version, OS</th><th>ID, '
            'Transfer, Links</th><th>Information</th><th>Progress</th></tr><br>')
        for i in fs.listdir('../saves'):
            save_file = open('../saves/' + str(i), 'r')
            txt = save_file.read().split('\n')
            ver, os, save, iden = txt[0].split(':')[0], txt[0].split(':')[1], str(i), txt[1]
            save_file.close()
            if ver == 'gb' and not config.gb_maint or ver == 'jp' and not config.jp_maint:
                try:
                    store = auth.login(ver, os, crypto.basic(iden), False)
                    if 'error' not in store:
                        if 'reason' not in store:
                            caches.load_account(save, iden, ver, os, store['access_token'], store['secret'])
                            store = ingame.user(ver, os, caches.sess_token, caches.sess_secret, False)
                            if 'error' not in store:
                                user = store['user']
                                areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                      caches.sess_secret)
                                cleared = 0
                                for a in areas['user_areas']:
                                    if a['area_id'] <= 27:
                                        if 'is_cleared_normal' in a:
                                            if a['is_cleared_normal']:
                                                cleared += 1
                                        elif 'is_cleared_hard' in a:
                                            if a['is_cleared_hard']:
                                                cleared += 1
                                        elif 'is_cleared_zhard' in a:
                                            if a['is_cleared_zhard']:
                                                cleared += 1
                                store = transfer.links(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                       caches.sess_secret)
                                if caches.acc_ver == 'gb':
                                    name = user['name']
                                    ver = 'Global'
                                else:
                                    name = user['name'].encode('UTF-16')
                                    ver = 'Japan'
                                f.write('<tr><td>' + str(i) + '<br>' + ver + '<br>' + os + '</td><td>' + str(
                                    user['id']) + '<br>' + store['external_links'][
                                            'link_code'] + '<br>Facebook: ' + store['external_links'][
                                            'facebook'] + '<br>Game center: ' + store['external_links'][
                                            'game_center'] + '<br>Google play: ' + store['external_links'][
                                            'google'] + '<br>Apple: ' +
                                        store['external_links']['apple'] + '</td><td>Name: ' + str(
                                    name) + '<br>Rank: ' + str(
                                    user['rank']) + '<br>Stones: ' + str(user['stone']) + '<br>Zeni: ' + str(
                                    user['zeni']) + '</td><td>Tutorial finished: ' + str(
                                    user['tutorial']['is_finished']) + '<br>Story cleared: ' + str(
                                    cleared) + '/27<br>Potential unlocked: ' + str(
                                    user['is_potential_releaseable']) + '</td></tr>')
                            else:
                                print('Error with: ' + str(i))
                                error.handler('suminfo', store)
                        else:
                            url = store['captcha_url']
                            key = store['captcha_session_key']
                            webbrowser.open(url, new=1, autoraise=True)
                            print(colors.render('{message}Complete CAPTCHA to login... Press ENTER when done.'))
                            input()
                            store = auth.login(ver, os, crypto.basic(iden), False, key)
                            if 'error' not in store:
                                caches.load_account(save, iden, ver, os, store['access_token'], store['secret'])
                                store = ingame.user(ver, os, caches.sess_token, caches.sess_secret, False)
                                if 'error' not in store:
                                    user = store['user']
                                    areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                          caches.sess_secret)
                                    cleared = 0
                                    for a in areas['user_areas']:
                                        if a['area_id'] <= 27:
                                            if 'is_cleared_normal' in a:
                                                if a['is_cleared_normal']:
                                                    cleared += 1
                                            elif 'is_cleared_hard' in a:
                                                if a['is_cleared_hard']:
                                                    cleared += 1
                                            elif 'is_cleared_zhard' in a:
                                                if a['is_cleared_zhard']:
                                                    cleared += 1
                                    store = transfer.links(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                           caches.sess_secret)
                                    if caches.acc_ver == 'gb':
                                        name = user['name']
                                        ver = 'Global'
                                    else:
                                        name = user['name'].encode('UTF-16')
                                        ver = 'Japan'
                                    f.write('<tr><td>' + str(i) + '<br>' + ver + '<br>' + os + '</td><td>' + str(
                                        user['id']) + '<br>' + store['external_links'][
                                                'link_code'] + '<br>Facebook: ' + store['external_links'][
                                                'facebook'] + '<br>Game center: ' + store['external_links'][
                                                'game_center'] + '<br>Google play: ' + store['external_links'][
                                                'google'] + '<br>Apple: ' +
                                            store['external_links']['apple'] + '</td><td>Name: ' + str(
                                        name) + '<br>Rank: ' + str(
                                        user['rank']) + '<br>Stones: ' + str(user['stone']) + '<br>Zeni: ' + str(
                                        user['zeni']) + '</td><td>Tutorial finished: ' + str(
                                        user['tutorial']['is_finished']) + '<br>Story cleared: ' + str(
                                        cleared) + '/27<br>Potential unlocked: ' + str(
                                        user['is_potential_releaseable']) + '</td></tr>')
                                else:
                                    print('Error with: ' + str(i))
                                    error.handler('suminfo', store)
                            else:
                                error.handler('sumcapt', store)
                    else:
                        print('Error with: ' + str(i))
                        error.handler('sumlog', store)
                except:
                    print('Error with: ' + str(i) + '\nCannot use this identifier!')
            else:
                print(colors.render('{error}[' + str(ver).upper() + '] servers are under maintenance!'))
        f.write('</table></body></html>')
        f.close()
        print(colors.render('{success}Summarization complete. Saved as: summaries/' + date + '.html'))
        caches.loaded = None
        return 1
    # convert
    if args[0].lower() == 'convert' and caches.loaded is None:
        for save in fs.listdir('../saves/'):
            if '.txt' not in save:
                acc_ver = None
                f = open('../saves/' + save, 'r')
                txt = f.read().rstrip().split('\n')
                f.close()
                if len(str(txt[0]).rstrip()) >= 100:
                    iden = txt[0]
                    if txt[4] == 'global':
                        acc_ver = 'gb'
                    elif txt[4] == 'japan':
                        acc_ver = 'jp'
                    if acc_ver == 'gb' or acc_ver == 'jp':
                        acc_os, ad_id, uuid = txt[3], txt[1], txt[2]
                        save_name = None
                        if fs.path.isfile('../saves/' + save + '.txt'):
                            print(colors.render('{error}this save name already exists! randomizing name...'))
                            save_name = str(save).lower() + str(randint(0, 99) + '-16')
                        else:
                            save_name = str(save).lower()
                        f = open('../saves/' + save_name + '.txt', 'w')
                        f.write(
                            str(acc_ver) + ':' + str(acc_os) + '\n' + str(iden) + '\n' + str(ad_id) + '\n' + str(uuid))
                        f.close()
                        fs.unlink('../saves/' + str(save))
                        print(colors.render('{success}converted "' + str(save) + '" to "' + save_name + '.txt"'))
                    else:
                        print(
                            colors.render('{error}unable to determine game version for save file "' + str(save) + '"'))
                else:
                    print(colors.render('{error}unknown save format.'))
        return 1
    # ===== tools =====
    # recover
    if args[0].lower() == 'recover' and caches.loaded is None:
        if len(args) == 4 and '' not in args:
            if args[1] == 'gb' and not config.gb_maint or args[1] == 'jp' and not config.jp_maint:
                if args[2] == 'ios' or args[2] == 'android':
                    if len(args[3]) >= 152:
                        iden = args[3]
                        store = auth.login(args[1], args[2], crypto.basic(iden), False)
                        if 'error' not in store:
                            if 'reason' not in store:
                                save = funcs.create_save_file(args[1], args[2], iden)
                                caches.load_account(save, iden, args[1], args[2], store['access_token'], store['secret'])
                                # funcs.help2()
                            else:
                                url = store['captcha_url']
                                key = store['captcha_session_key']
                                webbrowser.open(url, new=1, autoraise=True)
                                print(colors.render('{message}Complete CAPTCHA to login... Press ENTER when done.'))
                                input()
                                store = auth.login(args[1], args[2], crypto.basic(iden), False, key)
                                if 'error' not in store:
                                    save = funcs.create_save_file(args[1], args[2], iden)
                                    caches.load_account(save, iden, args[1], args[2], store['access_token'], store['secret'])
                                    # funcs.help2()
                                else:
                                    error.handler('rlogin2', store)
                        else:
                            error.handler('rlogin', store)
                    else:
                        print(colors.render('{error}not a valid identifier.'))
                else:
                    print(colors.render('{error}invalid OS input.'))
            else:
                if args[1] == 'gb' and config.gb_maint or args[1] == 'jp' and config.jp_maint:
                    print(colors.render('{error}[' + str(args[1]).upper() + '] servers are under maintenance!'))
                else:
                    print(colors.render('{error}invalid version input.'))
        else:
            print(colors.render('{error}recover gb/jp ios/android identifier'))
        return 0
    # ===== other =====
    # settings
    if args[0].lower() == 'settings':
        if len(args) >= 2 and '' not in args:
            if args[1] == 'color':
                if len(args) == 4:
                    color = ['red', 'green', 'cyan', 'blue', 'yellow', 'white', 'purple']
                    if args[2] == 'commands':
                        settings = funcs.get_settings()
                        for i in color:
                            if str(args[3]).lower() == str(i):
                                settings['colors']['command'] = str(args[3]).lower()
                        funcs.save_settings(settings)
                        print(colors.render('{success}color settings saved.'))
                    if args[2] == 'descriptions':
                        settings = funcs.get_settings()
                        for i in color:
                            if str(args[3]).lower() == str(i):
                                settings['colors']['description'] = str(args[3]).lower()
                        funcs.save_settings(settings)
                        print(colors.render('{success}color settings saved.'))
                    if args[2] == 'error':
                        settings = funcs.get_settings()
                        for i in color:
                            if str(args[3]).lower() == str(i):
                                settings['colors']['error'] = str(args[3]).lower()
                        funcs.save_settings(settings)
                        print(colors.render('{success}color settings saved.'))
                    if args[2] == 'success':
                        settings = funcs.get_settings()
                        for i in color:
                            if str(args[3]).lower() == str(i):
                                settings['colors']['success'] = str(args[3]).lower()
                        funcs.save_settings(settings)
                        print(colors.render('{success}color settings saved.'))
                    if args[2] == 'message':
                        settings = funcs.get_settings()
                        for i in color:
                            if str(args[3]).lower() == str(i):
                                settings['colors']['message'] = str(args[3]).lower()
                        funcs.save_settings(settings)
                        print(colors.render('{success}color settings saved.'))
                    if args[2] == 'drops':
                        settings = funcs.get_settings()
                        for i in color:
                            if str(args[3]).lower() == str(i):
                                settings['colors']['drops'] = str(args[3]).lower()
                        funcs.save_settings(settings)
                        print(colors.render('{success}color settings saved.'))
                else:
                    print(
                        'settings color <text> <color>\n-- Text types --\ncommands - command in help.\ndescriptions - '
                        'command details in help.\nerror - error text.\nsuccess - success text.\nmessage - messages '
                        'color.\ndrops - rewards/drops color.\n-- Color types '
                        '--\nred\ngreen\ncyan\nblue\nyellow\nwhite\npurple')
        else:
            print('--- List of settings ---\ncolor - set color of text.')
        return 1
    # support
    if args[0].lower() == 'support':
        webbrowser.open(config.x0a1_0[5], new=1, autoraise=True)
        return 1
    # exit
    if args[0].lower() == 'exit':
        if caches.loaded is None:
            exit()
        else:
            caches.loaded = None
            funcs.navigator(0)
            return 1
    # ===== farmbot =====
    # awaken
    # baba
    if args[0].lower() == 'baba' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'list':
                if len(args) >= 3:
                    if args[2] == 'bp':
                        store = ingame.baba_items(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                 'exchange_point')
                        if 'error' not in store:
                            for i in store['shop_on_sale_items']:
                                if i['buyable']:
                                    for j in i['shop_items']:
                                        if j['item_type'] == 'Card':
                                            try:
                                                element = ''
                                                db_ele = \
                                                    database.fetch(caches.acc_ver + '.db', 'cards',
                                                                   'id=' + str(j['item_id']))[
                                                        13]
                                                if db_ele is 0 or db_ele is 10 or db_ele is 20:
                                                    element = Fore.CYAN + 'AGL'
                                                if db_ele is 1 or db_ele is 11 or db_ele is 21:
                                                    element = Fore.GREEN + 'TEQ'
                                                if db_ele is 2 or db_ele is 12 or db_ele is 22:
                                                    element = Fore.MAGENTA + 'INT'
                                                if db_ele is 3 or db_ele is 13 or db_ele is 23:
                                                    element = Fore.RED + 'STR'
                                                if db_ele is 4 or db_ele is 14 or db_ele is 24:
                                                    element = Fore.YELLOW + 'PHY'
                                                print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' + element + ' ' +
                                                      database.fetch(caches.acc_ver + '.db', 'cards',
                                                                     'id=' + str(j['item_id']))[1] + ' [' +
                                                      database.fetch(caches.acc_ver + '.db', 'leader_skills',
                                                                     'id=' + str(
                                                                         database.fetch(caches.acc_ver + '.db', 'cards',
                                                                                        'id=' + str(j['item_id']))[
                                                                             24]))[1] + '] x' + str(
                                                    j['quantity']) + ' (' + str(i['discount_price']) + 'bp)')
                                            except:
                                                print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' + 'card x' + str(
                                                    j['quantity']) + ' (' + str(i['discount_price']) + 'bp)')
                                        if j['item_type'] == 'SupportItem':
                                            print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' +
                                                  database.fetch(caches.acc_ver + '.db', 'support_items',
                                                                 'id=' + str(j['item_id']))[1] + ' x' + str(
                                                j['quantity']) + ' (' + str(i['discount_price']) + 'bp)')
                                        if j['item_type'] == 'AwakeningItem':
                                            print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' +
                                                  database.fetch(caches.acc_ver + '.db', 'awakening_items',
                                                                 'id=' + str(j['item_id']))[1] + ' x' + str(
                                                j['quantity']) + ' (' + str(i['discount_price']) + 'bp)')
                                        if j['item_type'] == 'TrainingItem':
                                            print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' +
                                                  database.fetch(caches.acc_ver + '.db', 'training_items',
                                                                 'id=' + str(j['item_id']))[1] + ' x' + str(
                                                j['quantity']) + ' (' + str(i['discount_price']) + 'bp)')
                        else:
                            error.handler('lsBP', store)
                    if args[2] == 'zeni':
                        store = ingame.baba_items(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                 'zeni')
                        for i in store['shop_on_sale_items']:
                            if i['buyable']:
                                for j in i['shop_items']:
                                    if j['item_type'] == 'Card':
                                        try:
                                            element = ''
                                            db_ele = \
                                                database.fetch(caches.acc_ver + '.db', 'cards',
                                                               'id=' + str(j['item_id']))[
                                                    13]
                                            if db_ele is 0 or db_ele is 10 or db_ele is 20:
                                                element = Fore.CYAN + 'AGL'
                                            if db_ele is 1 or db_ele is 11 or db_ele is 21:
                                                element = Fore.GREEN + 'TEQ'
                                            if db_ele is 2 or db_ele is 12 or db_ele is 22:
                                                element = Fore.MAGENTA + 'INT'
                                            if db_ele is 3 or db_ele is 13 or db_ele is 23:
                                                element = Fore.RED + 'STR'
                                            if db_ele is 4 or db_ele is 14 or db_ele is 24:
                                                element = Fore.YELLOW + 'PHY'
                                            print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' + element + ' ' +
                                                  database.fetch(caches.acc_ver + '.db', 'cards',
                                                                 'id=' + str(j['item_id']))[1] + ' [' +
                                                  database.fetch(caches.acc_ver + '.db', 'leader_skills', 'id=' + str(
                                                      database.fetch(caches.acc_ver + '.db', 'cards',
                                                                     'id=' + str(j['item_id']))[24]))[1] + '] x' + str(
                                                j['quantity']) + ' (' + str(i['discount_price']) + 'zeni)')
                                        except:
                                            print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' + 'card x' + str(
                                                j['quantity']) + ' (' + str(i['discount_price']) + 'zeni)')
                                    if j['item_type'] == 'SupportItem':
                                        print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' +
                                              database.fetch(caches.acc_ver + '.db', 'support_items',
                                                             'id=' + str(j['item_id']))[1] + ' x' + str(
                                            j['quantity']) + ' (' + str(i['discount_price']) + 'zeni)')
                                    if j['item_type'] == 'AwakeningItem':
                                        print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' +
                                              database.fetch(caches.acc_ver + '.db', 'awakening_items',
                                                             'id=' + str(j['item_id']))[1] + ' x' + str(
                                            j['quantity']) + ' (' + str(i['discount_price']) + 'zeni)')
                                    if j['item_type'] == 'TrainingItem':
                                        print(Fore.LIGHTWHITE_EX + '#' + str(i['id']) + ' ' +
                                              database.fetch(caches.acc_ver + '.db', 'training_items',
                                                             'id=' + str(j['item_id']))[1] + ' x' + str(
                                            j['quantity']) + ' (' + str(i['discount_price']) + 'zeni)')
                    if args[2] == 'treasure':
                        store = ingame.baba_items(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                 'treasure')
                        if 'error' not in store:
                            for i in store['shop_on_sale_treasure_items']:
                                try:
                                    print(colors.render('{message}\n----- Treasure: ' + str(
                                        database.fetch(caches.acc_ver + '.db', 'treasure_items',
                                                       'id=' + str(i['treasure_item_id']))[1]) + ' -----'))
                                except:
                                    print(colors.render(
                                        '{message}\n----- Treasure: ' + str(i['treasure_item_id']) + ' -----'))
                                for x in i['shop_on_sale_items']:
                                    if x['buyable']:
                                        print('#' + str(x['id']))
                                        if 'discount_price' in x:
                                            print('Discount: ' + str(x['discount_price']))
                                        print('Price: ' + str(x['price']))
                                        if 'is_display_remaining_time' in x:
                                            if x['is_display_remaining_time']:
                                                print('Ends: ' + str(x['end_at']))
                                        print('Max: ' + str(x['buyable_num']))
                                        for j in x['shop_items']:
                                            if 'Card' in j['item_type']:
                                                try:
                                                    element = ''
                                                    db_ele = database.fetch(caches.acc_ver + '.db', 'cards',
                                                                            'id=' + str(j['item_id']))[13]
                                                    if db_ele is 0 or db_ele is 10 or db_ele is 20:
                                                        element = Fore.CYAN + 'AGL'
                                                    if db_ele is 1 or db_ele is 11 or db_ele is 21:
                                                        element = Fore.GREEN + 'TEQ'
                                                    if db_ele is 2 or db_ele is 12 or db_ele is 22:
                                                        element = Fore.MAGENTA + 'INT'
                                                    if db_ele is 3 or db_ele is 13 or db_ele is 23:
                                                        element = Fore.RED + 'STR'
                                                    if db_ele is 4 or db_ele is 14 or db_ele is 24:
                                                        element = Fore.YELLOW + 'PHY'
                                                    print(
                                                        element + ' ' + database.fetch(caches.acc_ver + '.db', 'cards',
                                                                                       'id=' + str(j['item_id']))[
                                                            1] + ' [' +
                                                        database.fetch(caches.acc_ver + '.db', 'leader_skills',
                                                                       'id=' + str(database.fetch(
                                                                           caches.acc_ver + '.db', 'cards',
                                                                           'id=' + str(j['item_id']))[24]))[
                                                            1] + '] x' + str(j['quantity']))
                                                except:
                                                    print('Item #' + str(j['item_id']))
                                                    print('Type: ' + str(j['item_type']))
                                                    print('Amount: ' + str(j['quantity']))
                                            elif j['item_type'] == 'SupportItem':
                                                print(Fore.LIGHTWHITE_EX +
                                                      database.fetch(caches.acc_ver + '.db', 'support_items',
                                                                     'id=' + str(j['item_id']))[1] + ' x' + str(
                                                    j['quantity']))
                                            elif j['item_type'] == 'AwakeningItem':
                                                print(Fore.LIGHTWHITE_EX +
                                                      database.fetch(caches.acc_ver + '.db', 'awakening_items',
                                                                     'id=' + str(j['item_id']))[1] + ' x' + str(
                                                    j['quantity']))
                                            elif j['item_type'] == 'TrainingItem':
                                                print(Fore.LIGHTWHITE_EX +
                                                      database.fetch(caches.acc_ver + '.db', 'training_items',
                                                                     'id=' + str(j['item_id']))[1] + ' x' + str(
                                                    j['quantity']))
                                            elif j['item_type'] == 'PotentialItem':
                                                print(Fore.LIGHTWHITE_EX +
                                                      database.fetch(caches.acc_ver + '.db', 'potential_items',
                                                                     'id=' + str(j['item_id']))[1] + ' x' + str(
                                                    j['quantity']))
                                            else:
                                                print('Item #' + str(j['item_id']))
                                                print('Type: ' + str(j['item_type']))
                                                print('Amount: ' + str(j['quantity']))
                        else:
                            error.handler('treasure', store)
                else:
                    print(colors.render('{error}missing argument. - baba list <bp/zeni/treasure>'))
            if args[1] == 'sell':
                if len(args) >= 4:
                    farmbot.baba_specific(args[2], int(args[3]))
                else:
                    farmbot.baba_specific(args[2])
            if args[1] == 'buy':
                if len(args) >= 5:
                    if args[2] == 'bp':
                        store = ingame.baba_buy(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                               'exchange_point', args[3], args[4])
                        if 'error' not in store:
                            print(store)
                        else:
                            error.handler('baba-bp', store)
                    if args[2] == 'zeni':
                        store = ingame.baba_buy(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                               'zeni', args[3], args[4])
                        if 'error' not in store:
                            print(store)
                        else:
                            error.handler('baba-zeni', store)
                else:
                    print('missing argument. - baba buy <bp/zeni> <id> <amount>')
            if args[1] == 'quick':
                farmbot.baba_useless()
        else:
            print(colors.render('{error}baba list/sell/buy'))
        return 0
    # banners
    if args[0].lower() == 'banners' and caches.loaded is not None:
        store = ingame.banners(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            for i in store['gashas']:
                print(Fore.LIGHTGREEN_EX + str(i['id']) + ' - ' + i['name'])
        else:
            error.handler('banners', store)
        return 0
    # box
    if args[0].lower() == 'box' and caches.loaded is not None:
        settings = funcs.get_settings()
        #print(caches.cards)
        rarity = []
        if len(args) >= 2 and str(args[1]).lower() in ['n', 'r', 'sr', 'ssr', 'ur', 'lr', 'items']:
            rarity.append(str(args[1]).lower())
        lr = []
        ur = []
        ssr = []
        sr = []
        r = []
        n = []
        if 'items' not in rarity:
            print(colors.render('{message}gathering cards...'))
            if not settings['display_only_ids']:
                for i in caches.cards:
                    card = json.loads(i[3])
                    card_rarity = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5]
                    if card_rarity == 5:
                        if len(rarity) == 0 or 'lr' in rarity:
                            card_text = funcs.render_card_text(card, False, False, True)
                            lr.append(card_text)
                    if card_rarity == 4:
                        if len(rarity) == 0 or 'ur' in rarity:
                            card_text = funcs.render_card_text(card, False, False, True)
                            ur.append(card_text)
                    if card_rarity == 3:
                        if len(rarity) == 0 or 'ssr' in rarity:
                            card_text = funcs.render_card_text(card, False, False, True)
                            ssr.append(card_text)
                    if card_rarity == 2:
                        if len(rarity) == 0 or 'sr' in rarity:
                            card_text = funcs.render_card_text(card, False, False, True)
                            sr.append(card_text)
                    if card_rarity == 1:
                        if len(rarity) == 0 or 'r' in rarity:
                            card_text = funcs.render_card_text(card, False, False, True)
                            r.append(card_text)
                    if card_rarity == 0:
                        if len(rarity) == 0 or 'n' in rarity:
                            card_text = funcs.render_card_text(card, False, False, True)
                            n.append(card_text)
                if len(rarity) == 0:
                    print(Fore.WHITE + '==== ==== > LR < ==== ====\n\n' + '\n'.join(
                        lr) + Fore.WHITE + '\n\n==== ==== > UR < ==== ====\n\n' + '\n'.join(
                        ur) + Fore.WHITE + '\n\n==== ==== > SSR < ==== ====\n\n' + '\n'.join(
                        ssr) + Fore.WHITE + '\n\n==== ==== > SR < ==== ====\n\n' + '\n'.join(
                        sr) + Fore.WHITE + '\n\n==== ==== > R < ==== ====\n\n' + '\n'.join(
                        r) + Fore.WHITE + '\n\n==== ==== > N < ==== ====\n\n' + '\n'.join(n))
                else:
                    if len(lr) != 0:
                        print(Fore.WHITE + '==== ==== > LR < ==== ====\n\n' + '\n'.join(lr))
                    if len(ur) != 0:
                        print(Fore.WHITE + '==== ==== > UR < ==== ====\n\n' + '\n'.join(ur))
                    if len(ssr) != 0:
                        print(Fore.WHITE + '==== ==== > SSR < ==== ====\n\n' + '\n'.join(ssr))
                    if len(sr) != 0:
                        print(Fore.WHITE + '==== ==== > SR < ==== ====\n\n' + '\n'.join(sr))
                    if len(r) != 0:
                        print(Fore.WHITE + '==== ==== > R < ==== ====\n\n' + '\n'.join(r))
                    if len(n) != 0:
                        print(Fore.WHITE + '==== ==== > N < ==== ====\n\n' + '\n'.join(n))
            else:
                for i in caches.cards:
                    i = json.loads(i[3])
                    print(str(i['card_id']) + '\n' + 'SA: ' + str(
                        i['skill_lv']) + ', Potential: ' + str(i['released_rate']) + '%, EXP: ' + str(
                        i['exp']) + ', uid: ' + str(i['id']))
        else:
            print(colors.render('{message}gathering item cards...'))
            if not settings['display_only_ids']:
                for i in caches.item_cards:
                    card_rarity = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[0]))[5]
                    if card_rarity == 5:
                        card_text = funcs.render_card_text({'card_id': i[0], 'quantity': i[1]}, True, False, False)
                        lr.append(card_text)
                    if card_rarity == 4:
                        card_text = funcs.render_card_text({'card_id': i[0], 'quantity': i[1]}, True, False, False)
                        ur.append(card_text)
                    if card_rarity == 3:
                        card_text = funcs.render_card_text({'card_id': i[0], 'quantity': i[1]}, True, False, False)
                        ssr.append(card_text)
                    if card_rarity == 2:
                        card_text = funcs.render_card_text({'card_id': i[0], 'quantity': i[1]}, True, False, False)
                        sr.append(card_text)
                    if card_rarity == 1:
                        card_text = funcs.render_card_text({'card_id': i[0], 'quantity': i[1]}, True, False, False)
                        r.append(card_text)
                    if card_rarity == 0:
                        card_text = funcs.render_card_text({'card_id': i[0], 'quantity': i[1]}, True, False, False)
                        n.append(card_text)
                print(Fore.WHITE + '==== ==== > LR < ==== ====\n\n' + '\n'.join(
                    lr) + Fore.WHITE + '\n\n==== ==== > UR < ==== ====\n\n' + '\n'.join(
                    ur) + Fore.WHITE + '\n\n==== ==== > SSR < ==== ====\n\n' + '\n'.join(
                    ssr) + Fore.WHITE + '\n\n==== ==== > SR < ==== ====\n\n' + '\n'.join(
                    sr) + Fore.WHITE + '\n\n==== ==== > R < ==== ====\n\n' + '\n'.join(
                    r) + Fore.WHITE + '\n\n==== ==== > N < ==== ====\n\n' + '\n'.join(n))
            else:
                for i in caches.item_cards:
                    print(str(i['card_id']) + ' x' + str(i['quantity']))
        return 0
    # capacity
    if args[0].lower() == 'capacity' and caches.loaded is not None:
        if len(args) == 2 and '' not in args:
            for i in range(int(args[1])):
                store = ingame.capacity(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in store:
                    print(colors.render('{success}box size increased by 5+'))
                else:
                    error.handler('capacity', store)
        else:
            store = ingame.capacity(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            if 'error' not in store:
                print(colors.render('{success}box size increased by 5+'))
            else:
                error.handler('capacity', store)
        return 0
    # clash
    if args[0].lower() == 'clash' and caches.loaded is not None:
        farmbot.streamline('clash')
        return 0
    # clear
    if args[0].lower() == 'clear' and caches.loaded is not None:
        # quests, events, eza, clash
        if len(args) == 2 and '' not in args:
            if args[1] == 'quests':
                farmbot.streamline('quests')
            if args[1] == 'events':
                farmbot.streamline('events')
            if args[1] == 'eza':
                farmbot.streamline('ezas')
            if args[1] == 'clash':
                farmbot.streamline('clash')
        else:
            print(colors.render('{error}clear quests/events/eza/clash'))
        return 0
    # dbs
    if args[0].lower() == 'dbs' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'list':
                store = ingame.dragonballs(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in store:
                    for i in store['dragonball_sets']:
                        if i['ball_type'] == 0:
                            print(Fore.GREEN + '==== ==== > Shenron < ==== ====\n' + Fore.WHITE)
                            for x in i['dragonballs']:
                                print(str(x['num']) + ' - collected: ' + str(x['is_got']) + ' (' + str(
                                    x['quest_id']) + ':' + str(x['difficulties'][0]) + ')')
                    for i in store['dragonball_sets']:
                        if i['ball_type'] == 1:
                            print(Fore.GREEN + '\n==== ==== > Porunga < ==== ====\n' + Fore.WHITE)
                            for x in i['dragonballs']:
                                print(str(x['num']) + ' - collected: ' + str(x['is_got']) + ' (' + str(
                                    x['description']) + ')')
                                if 'condition' in x['mission']:
                                    print(str(x['mission']['conditions']))
                else:
                    error.handler('dragonballs', store)
            if args[1] == 'seek':
                store = ingame.dragonballs(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in store:
                    for i in store['dragonball_sets']:
                        if i['ball_type'] == 0:
                            for x in i['dragonballs']:
                                if not x['is_got']:
                                    farmbot.handler(0, str(x['quest_id']), str(x['difficulties'][0]))
                else:
                    error.handler('dragonballs', store)
            if args[1] == 'wish':
                if len(args) == 2:
                    store = ingame.dragon_wish(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, 1, None)
                    if 'error' not in store:
                        for i in store['dragonball_wishes']:
                            if i['is_wishable']:
                                print(Fore.LIGHTGREEN_EX + '#' + str(i['id']) + ' - ' + str(
                                    i['title']) + '\n' + Fore.LIGHTCYAN_EX + '(' + str(i['description']) + ')')
                        print(Fore.LIGHTYELLOW_EX + 'use "dbs wish <id>" to make the wish.')
                    else:
                        error.handler('info user', store)
                elif len(args) == 3:
                    wishes = [int(args[2])]
                    store = ingame.dragon_wish(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, 1, wishes)
                    if 'error' not in store:
                        print(colors.render('{success}Arise Shenron & grant my wish!'))
                        farmbot.gifts()
                    else:
                        error.handler('wish', store)
                else:
                    print(colors.render('{error}dbs <wish> / dbs <wish> <number>'))
        else:
            print(colors.render('{error}dbs <list/seek/wish>'))
        return 0
    # event
    if args[0].lower() == 'event' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'list':
                store = caches.events
                for i in store['events']:
                    try:
                        if 'quests' in i:
                            print(Fore.LIGHTRED_EX + '===> ' + str(
                                database.fetch(caches.acc_ver + '.db', 'areas', 'id=' + str(i['id']))[4]) + ' <===')
                            for x in i['quests']:
                                difficulties = []
                                for j in database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps',
                                                           'quest_id=' + str(x['id'])):
                                    difficulties.append(str(j[2]))
                                print(Fore.LIGHTYELLOW_EX + str(x['id']) + ' (' + ', '.join(
                                    difficulties) + ')' + Fore.LIGHTRED_EX + ' - ' + Fore.LIGHTGREEN_EX + str(
                                    x['name']))
                    except:
                        print(Fore.LIGHTRED_EX + '===> unknown <===')
                        for x in i['quests']:
                            print(Fore.LIGHTYELLOW_EX + str(
                                x['id']) + Fore.LIGHTRED_EX + ' - ' + Fore.LIGHTGREEN_EX + str(x['name']))
            if args[1] == 'area':
                if len(args) >= 3:
                    if len(args[2]) >= 3 and len(args[2]) <= 6:
                        store = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                        if 'error' not in store:
                            maps = []
                            if len(args[2]) > 3:
                                print('you provided a stage ID not area ID; trimming stage ID...')
                                args[2] = args[2][:-3]
                            for i in store['user_areas']:
                                if int(i['area_id']) == int(args[2]):
                                    for j in i['user_sugoroku_maps']:
                                        farmbot.handler(0, str(str(j['sugoroku_map_id'])[:-1]), str(j['sugoroku_map_id'])[-1])
                        else:
                            error.handler('quests', store)
                    else:
                        print('invalid area ID')
                else:
                    print('no area ID provided.')
            if args[1] == 'stage':
                if len(args) >= 5:
                    if len(args[2]) >= 4 and len(args[2]) <= 6:
                        if len(args[3]) == 1:
                            if int(args[4]) != 0:
                                for i in range(int(args[4])):
                                    farmbot.handler(0, str(args[2]), args[3])
                            else:
                                print(colors.render('{error}can\'t run stage 0 times!'))
                        else:
                            print(colors.render('{error}difficulty is wrong.\n0=normal || 1=hard || 2=zhard || 3=super || 4=super2'))
                    else:
                        print(colors.render('{error}invalid stage ID length.'))
                else:
                    print(colors.render('{error}event stage <stage id> <difficulty> <runs>'))
            if args[1] == 'keys':
                store = caches.events
                print(store['eventkagi_events'][0])
                for i in store['eventkagi_events']:
                    try:
                        if 'quests' in i:
                            print(Fore.LIGHTRED_EX + '===> ' + str(
                                database.fetch(caches.acc_ver + '.db', 'areas', 'id=' + str(i['id']))[4]) + ' <===')
                            for x in i['quests']:
                                difficulties = []
                                for j in database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps',
                                                           'quest_id=' + str(x['id'])):
                                    difficulties.append(str(j[2]))
                                print(Fore.LIGHTYELLOW_EX + str(x['id']) + ' (' + ', '.join(
                                    difficulties) + ')' + Fore.LIGHTRED_EX + ' - ' + Fore.LIGHTGREEN_EX + str(
                                    x['name']))
                    except:
                        print(Fore.LIGHTRED_EX + '===> unknown <===')
                        for x in i['quests']:
                            print(Fore.LIGHTYELLOW_EX + str(
                                x['id']) + Fore.LIGHTRED_EX + ' - ' + Fore.LIGHTGREEN_EX + str(x['name']))
        else:
            print(colors.render('{error}event list/area/stage/keys/key'))
        return 0
    # eza
    if args[0].lower() == 'eza' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'list':
                store = caches.events
                for x in store['z_battle_stages']:
                    try:
                        print(str(x['id']) + ' ' + database.fetch(caches.acc_ver + '.db', 'z_battle_stage_views',
                                                                  'z_battle_stage_id=' + str(x['id']))[3] + ' - ' +
                              database.fetch(caches.acc_ver + '.db', 'z_battle_stage_views',
                                             'z_battle_stage_id=' + str(x['id']))[2])
                    except:
                        print(str(x['id']) + ' - unknown')
            if args[1] == 'clear':
                if len(args) >= 3:
                    store = caches.events
                    eza_pool = []
                    for x in store['z_battle_stages']:
                        eza_pool.append(int(x['id']))
                    if int(args[2]) in eza_pool:
                        store = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                        if 'error' not in store:
                            for x in store['user_z_battles']:
                                if x['z_battle_stage_id'] == int(args[2]):
                                    clear_count = x['max_clear_level']
                                    if int(clear_count) == 0:
                                        clear_count = 1
                                    while int(clear_count) <= 30:
                                        farmbot.run_z_lvl(int(args[2]), int(clear_count))
                                        clear_count = clear_count + 1
                        else:
                            error.handler('ezaAreas', store)
                    else:
                        print(colors.render('{error}EZA event ID not in active pool!'))
                else:
                    print('missing EZA event ID.')
            if args[1] == 'level':
                if len(args) >= 3:
                    clear_times = 1
                    store = caches.events
                    eza_pool = []
                    for x in store['z_battle_stages']:
                        eza_pool.append(int(x['id']))
                    if int(args[2]) in eza_pool:
                        if len(args) == 4 and int(args[4]) != 0:
                            clear_times = int(args[4])
                        else:
                            print(colors.render('{error}You can\'t run 0 time(s)!\nclearing level once instead...'))
                        for i in range(clear_times + 1):
                            if int(i) != 0:
                                farmbot.run_z_lvl(int(args[2]), int(args[3]))
                    else:
                        print(colors.render('{error}EZA event ID not in active pool!'))
                else:
                    print('eza level <eza id> <level> <run amount>')
            if args[1] == 'exact':
                if len(args) >= 3:
                    currently_cleared = int(args[3])
                    store = caches.events
                    eza_pool = []
                    for x in store['z_battle_stages']:
                        eza_pool.append(int(x['id']))
                    while True:
                        if int(args[2]) in eza_pool:
                            if currently_cleared <= int(args[4]):
                                farmbot.run_z_lvl(int(args[2]), currently_cleared)
                                currently_cleared = currently_cleared + 1
                            else:
                                print(colors.render('{success}done farming EZA levels ' + args[3] + ' to ' + args[4]))
                                return
                        else:
                            print(colors.render('{error}EZA event ID not in active pool!'))
                            return
                else:
                    print('eza exact <eza id> <x lvl> <z lvl>')
            if args[1] == 'all':
                farmbot.streamline('ezas')
        else:
            print(colors.render('{error}eza list/clear/level/exact/all'))
        return 0
    # farm
    if args[0].lower() == 'farm' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'medal':
                if len(args) == 6:
                    print(colors.render('{message}farming for ' + str(args[4]) + ' medals...'))
                    medals = 0
                    max = int(args[4])
                    runs = 0
                    medal_id = int(args[5])
                    # we could easily divide the required amount to the drops but some drops are randomized; this won't suffice.
                    while medals < max:
                        drops = farmbot.handler(0, str(args[2]), str(args[3]), None, True)
                        if drops is not None:
                            if drops:
                                runs += 1
                                for i in drops['items']:
                                    if i['item_type'] == 'AwakeningItem':
                                        if int(i['item_id']) == medal_id:
                                            medals += int(i['quantity'])
                                            print(colors.render('{success}current count: ' + str(medals)))
                        else:
                            medals = max
                            print(colors.render('{error}No drops... is the event up?'))
                    print(colors.render(
                        '{success}done farming medals. ' + str(runs) + ' runs - ' + str(medals) + ' medals.'))
                    funcs.refresh()
                else:
                    print('farm medal <stage> <difficulty> <amount> <medal ID>')
            if args[1] == 'dupe':
                if len(args) == 6:
                    print(colors.render('{message}farming for ' + str(args[4]) + ' dupes...'))
                    dupes = 0
                    max = int(args[4])
                    runs = 0
                    chara_id = int(args[5])
                    while dupes < max:
                        drops = farmbot.handler(0, str(args[2]), str(args[3]), None, True)
                        time.sleep(1)
                        if drops is not None:
                            if drops:
                                runs += 1
                                for i in drops['items']:
                                    if i['item_type'] == 'Card':
                                        if int(i['item_id']) == chara_id:
                                            dupes += int(i['quantity'])
                                            print(colors.render('{success}current count: ' + str(dupes)))
                        else:
                            dupes = max
                            print(colors.render('{error}No drops... is the event up?'))
                    print(colors.render(
                        '{success}done farming dupes. ' + str(runs) + ' runs - ' + str(dupes) + ' dupes.'))
                    funcs.refresh()
                else:
                    print('farm dupe <stage> <difficulty> <amount> <card id>')
            if args[1] == 'zeni':
                if len(args) == 3:
                    print(colors.render('{message}farming for ' + str(args[2]) + ' zeni...'))
                    zeni = 0
                    max = int(args[2])
                    runs = 0
                    base_amount = 0
                    ran_event = False
                    clear_count = 0
                    eza_id = None
                    store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
                    if 'error' not in store:
                        user = store['user']
                        base_amount = int(user['zeni'])
                    else:
                        error.handler('zeniUsr', store)
                    while zeni < max:
                        if not ran_event:
                            farmbot.handler(0, '116001', '2')
                            ran_event += True
                        store = caches.events
                        eza_pool = []
                        for x in store['z_battle_stages']:
                            eza_pool.append(int(x['id']))
                        store = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                        for i in eza_pool:
                            for x in store['user_z_battles']:
                                if int(x['z_battle_stage_id']) == int(i):
                                    clear_count = int(x['max_clear_level'])
                                    if clear_count != 999:
                                        eza_id = int(i)
                                        clear_count = clear_count + 1
                                        break
                                    else:
                                        continue
                        farmbot.run_z_lvl(int(eza_id), int(clear_count))
                        runs += 1
                        farmbot.sell_useless() # TODO sell items
                        store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
                        if 'error' not in store:
                            user = store['user']
                            zeni = int(user['zeni']) - base_amount
                            print(colors.render('{success}current amount: ' + str(zeni)))
                        else:
                            error.handler('zeniUsr2', store)
                    print(colors.render('{success}done farming zeni. ' + str(runs) + ' runs - ' + str(zeni) + ' zeni.'))
                    funcs.refresh()
                else:
                    print('farm zeni <amount>')
            if args[1] == 'rank':
                if len(args) == 3:
                    areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                    if 'error' not in areas:
                        cleared = 0
                        for i in areas['user_areas']:
                            if i['area_id'] <= 27:
                                if 'is_cleared_normal' in i:
                                    if i['is_cleared_normal']:
                                        cleared += 1
                                elif 'is_cleared_hard' in i:
                                    if i['is_cleared_hard']:
                                        cleared += 1
                                elif 'is_cleared_zhard' in i:
                                    if i['is_cleared_zhard']:
                                        cleared += 1
                        if cleared == 27:
                            print(colors.render('{message}farming for ' + str(args[2]) + ' rank(s)...'))
                            rank = 0
                            max = int(args[2])
                            runs = 0
                            base_amount = 0
                            ran_event = False
                            store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                False)
                            if 'error' not in store:
                                user = store['user']
                                base_amount = int(user['rank'])
                            else:
                                error.handler('rnkUsr', store)
                            while rank < max:
                                if not ran_event:
                                    farmbot.handler(0, '135002', '3')
                                    farmbot.handler(0, '135001', '1')
                                    ran_event += True
                                farmbot.handler(0, '27003', '3')
                                runs += 1
                                store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                    caches.sess_secret,
                                                    False)
                                if 'error' not in store:
                                    user = store['user']
                                    rank = int(user['rank']) - base_amount
                                    print(colors.render('{success}current count: ' + str(rank)))
                                else:
                                    error.handler('rnkUsr2', store)
                            print(colors.render(
                                '{success}done farming rank. ' + str(runs) + ' runs - ' + str(rank) + ' rank(s)'))
                            funcs.refresh()
                        else:
                            print(colors.render('{error}You haven\'t cleared story to use this command.'))
                    else:
                        error.handler('rAreas', areas)
                else:
                    print('farm rank <how many>')
            if args[1] == 'gem':
                if len(args) == 3:
                    areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                    if 'error' not in areas:
                        cleared = 0
                        for i in areas['user_areas']:
                            if i['area_id'] <= 27:
                                if 'is_cleared_normal' in i:
                                    if i['is_cleared_normal']:
                                        cleared += 1
                                elif 'is_cleared_hard' in i:
                                    if i['is_cleared_hard']:
                                        cleared += 1
                                elif 'is_cleared_zhard' in i:
                                    if i['is_cleared_zhard']:
                                        cleared += 1
                        if cleared == 27:
                            print(colors.render('{message}farming for ' + str(args[2]) + ' gems...'))
                            gems = 0
                            max = int(args[2])
                            runs = 0
                            base_amount = 0
                            store = ingame.get_items(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                    caches.sess_secret)
                            if 'error' not in store:
                                for i in store['treasure_items']['user_treasure_items']:
                                    if int(i['treasure_item_id']) == 1:
                                        base_amount = int(i['quantity'])
                            else:
                                error.handler('itms', store)
                            while gems < max:
                                farmbot.handler(0, '23005', '3')
                                runs += 1
                                store = ingame.get_items(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                        caches.sess_secret)
                                if 'error' not in store:
                                    for i in store['treasure_items']['user_treasure_items']:
                                        if int(i['treasure_item_id']) == 1:
                                            gems = int(i['quantity']) - base_amount
                                            print(colors.render('{success}current count: ' + str(gems)))
                                else:
                                    error.handler('itms2', store)
                            print(colors.render(
                                '{success}done farming gems. ' + str(runs) + ' runs - ' + str(gems) + ' gems.'))
                        else:
                            print(colors.render('{error}You haven\'t cleared story to use this command.'))
                    else:
                        error.handler('gAreas', areas)
                else:
                    print('farm gem <amount>')
            if args[1] == 'fp':
                pass
            if args[1] == 'kaistone':
                pass
        else:
            print(colors.render('{error}missing arguments.\nfarm <medal/dupe/zeni/rank/gem>'))
        return 0
    # favorite
    if args[0].lower() == 'favorite' and caches.loaded is not None:
        if len(args) == 2 and '' not in args:
            store = ingame.favorite_card(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, args[1])
            if 'error' not in store:
                card_ids = [store['card']]
                caches.update_cards(card_ids, None)
                print(colors.render('{success}card has been locked.'))
                # {'card': {'id': 1034115975, 'card_id': 1001890, 'exp': 7555, 'skill_lv': 1, 'is_favorite': True, 'awakening_route_id': None, 'is_released_potential': False, 'released_rate': 0.0, 'optimal_awakening_step': None, 'card_decoration_id': None, 'awakenings': [], 'unlocked_square_statuses': [], 'updated_at': 1607352047, 'created_at': 1570842893, 'potential_parameters': [], 'equipment_skill_items': [], 'link_skill_lvs': []}}
            else:
                error.handler('lock', store)
        else:
            print(colors.render('{error}favorite <card uid>'))
        return 0
    # friends
    if args[0].lower() == 'friends' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'list':
                store = ingame.friends(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in store:
                    print(colors.render('{message}==== ==== > Friends < ==== ====\n' + Fore.WHITE))
                    for i in store['friendships']:
                        card_text = funcs.render_card_text(i, False, False, True, True)
                        print(str(i['id']) + ', ' + str(i['user']['name']) + ', ' + str(
                            i['user']['rank']) + '\n' + card_text)
                    print(colors.render('{message}==== ==== > Pending < ==== ====\n' + Fore.WHITE))
                    for i in store['pending_friendships']:
                        card_text = funcs.render_card_text(i, False, False, True, True)
                        print(str(i['id']) + ', ' + str(i['user']['name']) + ', ' + str(
                            i['user']['rank']) + '\n' + card_text)
                else:
                    error.handler('friends', store)
            if args[1] == 'accept':
                if len(args) >= 3:
                    store = ingame.accept_friend(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                args[1])
                    if 'error' not in store:
                        if 'accepted' in store['friendship']['status']:
                            print(colors.render('{success}friend accepted.'))
                        else:
                            print(colors.render('{error}can\'t accept.'))
                    else:
                        error.handler('accept friend', store)
                else:
                    print(colors.render('{error}missing user/friend ID.'))
            if args[1] == 'search':
                if len(args) >= 3:
                    store = ingame.find_friend(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                              int(args[1]))
                    if 'error' not in store:
                        element = '?'
                        db_ele = database.fetch(caches.acc_ver + '.db', 'cards',
                                                'id=' + str(store['user']['leader']['card_id']))[
                            13]
                        if db_ele is 0 or db_ele is 10 or db_ele is 20:
                            element = Fore.CYAN + 'AGL'
                        if db_ele is 1 or db_ele is 11 or db_ele is 21:
                            element = Fore.GREEN + 'TEQ'
                        if db_ele is 2 or db_ele is 12 or db_ele is 22:
                            element = Fore.MAGENTA + 'INT'
                        if db_ele is 3 or db_ele is 13 or db_ele is 23:
                            element = Fore.RED + 'STR'
                        if db_ele is 4 or db_ele is 14 or db_ele is 24:
                            element = Fore.YELLOW + 'PHY'
                        print(str(store['user']['id']) + ', ' + str(store['user']['name']) + ', ' + str(
                            store['user']['rank']) + '\n' + element + ' ' +
                              database.fetch(caches.acc_ver + '.db', 'cards',
                                             'id=' + str(store['user']['leader']['card_id']))[
                                  1] + ' [' + database.fetch(caches.acc_ver + '.db', 'leader_skills', 'id=' + str(
                            database.fetch(caches.acc_ver + '.db', 'cards',
                                           'id=' + str(store['user']['leader']['card_id']))[24]))[
                                  1] + '],\nSA: ' + str(store['user']['leader']['skill_lv']) + '/' + str(
                            database.fetch(caches.acc_ver + '.db', 'cards',
                                           'id=' + str(store['user']['leader']['card_id']))[
                                15]) + ', Potential: ' + str(store['user']['leader']['released_rate']) + '%, Lvl: ' +
                              str(database.fetch(caches.acc_ver + '.db', 'card_exps',
                                                 'exp_total=' + str(store['user']['leader']['exp'])))[1] + '/' + str(
                            database.fetch(caches.acc_ver + '.db', 'cards',
                                           'id=' + str(store['user']['leader']['card_id']))[14]))
                    else:
                        error.handler('find friend', store)
                else:
                    print(colors.render('{error}missing user/friend ID.'))
            if args[1] == 'request':
                if len(args) >= 3:
                    store = ingame.add_friend(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                             args[1])
                    if 'error' not in store:
                        print(colors.render('{success}request sent.'))
                    else:
                        error.handler('add friend', store)
                else:
                    print(colors.render('{error}missing user/friend ID.'))
        else:
            print(colors.render('{error}friend list/accept/search/request'))
        return 0
    # gift
    if args[0].lower() == 'gift' and caches.loaded is not None:
        farmbot.gifts()
        farmbot.missions()
        return 0
    # help
    if args[0].lower() == 'help':
        if caches.loaded is None:
            funcs.navigator(0)
            # finally added examples cus' weyfol
        else:
            if len(args) == 2 and '' not in args:
                if int(args[1]) >= 1 and int(args[1]) <= 8:
                    funcs.navigator(int(args[1]))
                else:
                    print(colors.render('{error}help <page>'))
            else:
                funcs.navigator(99)
        return 1
    # history
    if args[0].lower() == 'history' and caches.loaded is not None:
        store = ingame.summon_history(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            print(Fore.LIGHTYELLOW_EX + '\n==== ==== > Stone < ==== ====\n')
            for i in store['histories']['stone']:
                print(Fore.LIGHTYELLOW_EX + str(i['name']) + ' - ' + str(
                    i['price']) + ' Stone(s)\n' + Fore.CYAN + datetime.utcfromtimestamp(int(i['drawn_at'])).strftime(
                    '%m/%d/%Y %H:%M.%S') + '\n' + Fore.WHITE + str(i['card_ids']) + '\n------------------------------')
            print(Fore.LIGHTBLUE_EX + '\n==== ==== > FP < ==== ====\n')
            for i in store['histories']['point']:
                print(Fore.LIGHTBLUE_EX + str(i['name']) + ' - ' + str(i[
                                                                           'price']) + ' FP\n' + Fore.CYAN + datetime.utcfromtimestamp(
                    int(i['drawn_at'])).strftime(
                    '%m/%d/%Y %H:%M.%S') + '\n' + Fore.WHITE + str(i['card_ids']) + '\n------------------------------')
            print(Fore.LIGHTRED_EX + '\n==== ==== > Tickets < ==== ====\n')
            for i in store['histories']['other']:
                print(Fore.LIGHTRED_EX + str(i['name']) + ' - ' + str(i[
                                                                          'price']) + ' Ticket(s)\n' + Fore.CYAN + datetime.utcfromtimestamp(
                    int(i['drawn_at'])).strftime(
                    '%m/%d/%Y %H:%M.%S') + '\n' + Fore.WHITE + str(i['card_ids']) + '\n------------------------------')
        else:
            error.handler('history', store)
        return 0
    # identifier
    if args[0].lower() == 'identifier' and caches.loaded is not None:
        print(caches.account)
        return 0
    # info
    if args[0].lower() == 'info' and caches.loaded is not None:
        store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
        if 'error' not in store:
            user = store['user']
            if int(user['boost_at']) < int(datetime.timestamp(datetime.now())):
                boost_count = 'unavailable'
            else:
                boost_count = str(user['boost_point']) + '/3'
            box = str(len(caches.cards))
            areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            cleared = 0
            for i in areas['user_areas']:
                if i['area_id'] <= 27:
                    if 'is_cleared_normal' in i:
                        if i['is_cleared_normal']:
                            cleared += 1
                    elif 'is_cleared_hard' in i:
                        if i['is_cleared_hard']:
                            cleared += 1
                    elif 'is_cleared_zhard' in i:
                        if i['is_cleared_zhard']:
                            cleared += 1
            print(colors.render('{success}-- Account info (' + str(
                caches.loaded) + ') --{message}\nVersion: ' + caches.acc_ver + '\nOS: ' + caches.acc_os + '\nID: ' + str(
                user['id']) + '\nName: ' + user['name'] + '\nRank: ' + str(user['rank']) + '\nStones: ' + str(
                user['stone']) + '\nStamina: ' + str(user['act']) + '/' + str(user['act_max']) + '\nZeni: ' + str(
                user['zeni']) + '\nFP: ' + str(user['gasha_point']) + '\nBP: ' + str(
                user['exchange_point']) + '\nCapacity: ' + box + '/' + str(
                user['total_card_capacity']) + '\nTeam cost: ' + str(
                user['team_cost_capacity']) + '\nFriends capacity: ' + str(
                user['friends_capacity']) + '\nBoost: ' + str(boost_count) + '\nWallpaper: #' + str(user[
                                                                                                                  'wallpaper_item_id']) + '\n{success}-- Progress --{message}' + '\nTutorial finished: ' + str(
                user['tutorial']['is_finished']) + '\nStory cleared: ' + str(cleared) + '/27\nPotential unlocked: ' + str(user['is_potential_releaseable'])))
        else:
            error.handler('infoUsr', store)
        return 0
    # items
    if args[0].lower() == 'items' and caches.loaded is not None:
        store = ingame.get_items(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            print(colors.render('{message}==== ==== > Support < ==== ====\n'))
            for i in store['support_items']['items']:
                try:
                    print(database.fetch(caches.acc_ver + '.db', 'support_items', 'id=' + str(i['item_id']))[
                              1] + ' x' + str(i['quantity']))
                except:
                    print('Support x' + str(i['quantity']))
            print(colors.render('\n{message}==== ==== > Training < ==== ====\n'))
            for i in store['training_items']:
                try:
                    print(database.fetch(caches.acc_ver + '.db', 'training_items', 'id=' + str(i['training_item_id']))[
                              1] + ' x' + str(i['quantity']))
                except:
                    print('Training x' + str(i['quantity']))
            print(colors.render('\n{message}==== ==== > Potential < ==== ====\n'))
            for i in store['potential_items']['user_potential_items']:
                try:
                    print(
                        database.fetch(caches.acc_ver + '.db', 'potential_items', 'id=' + str(i['potential_item_id']))[
                            1] + ' x' + str(i['quantity']))
                except:
                    print('Orb x' + str(i['quantity']))
            print(colors.render('\n{message}==== ==== > Treasure < ==== ====\n'))
            for i in store['treasure_items']['user_treasure_items']:
                try:
                    print(database.fetch(caches.acc_ver + '.db', 'treasure_items', 'id=' + str(i['treasure_item_id']))[
                              1] + ' x' + str(i['quantity']))
                except:
                    print('Treasure x' + str(i['quantity']))
            print(colors.render('\n{message}==== ==== > Special < ==== ====\n'))
            for i in store['special_items']:
                try:
                    print(database.fetch(caches.acc_ver + '.db', 'special_items', 'id=' + str(i['special_item_id']))[
                              1] + ' x' + str(i['quantity']))
                except:
                    print('Special x' + str(i['quantity']))
        else:
            error.handler('items', store)
        return 0
    # legend
    if args[0].lower() == 'legend' and caches.loaded is not None:
        print('this will be coming in a later update. Cheers!')
    # link
    if args[0].lower() == 'link' and caches.loaded is not None:
        if len(args) == 2 and '' not in args:
            if args[1] == 'list' or args[1] == 'fb' or args[1] == 'unlink':
                if args[1] == 'list':
                    store = transfer.links(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                    if 'error' not in store:
                        print(Fore.LIGHTYELLOW_EX + 'Facebook: ' + store['external_links'][
                            'facebook'] + '\nGame center: ' + store['external_links'][
                                  'game_center'] + '\nGoogle play: ' + store['external_links']['google'] + '\nApple: ' +
                              store['external_links']['apple'] + '\nTransfer code: ' + store['external_links'][
                                  'link_code'])
                    else:
                        error.handler('link-list', store)
                if args[1] == 'fb':
                    url = facebook.loginPage(caches.acc_ver)
                    facebook.webView(caches.acc_ver, caches.acc_os, url, 2, caches.sess_token, caches.sess_secret)
                if args[1] == 'unlink':
                    store = transfer.facebookUnlink(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                    caches.sess_secret)
                    if 'error' not in store:
                        print(colors.render('{success}account unlinked.'))
                    else:
                        error.handler('unlink', store)
            else:
                print('link <list/fb/unlink>')
        else:
            print('link <list/fb/unlink>')
        return 1
    # meat
    if args[0].lower() == 'meat' and caches.loaded is not None:
        store = ingame.login_resources(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            for i in store['act_items']:
                try:
                    item = database.fetch(caches.acc_ver + '.db', 'act_items', 'id=' + str(i['act_item_id']))
                    print(str(item[1]) + ' x' + str(i['quantity']) + '\n"' + str(item[2]) + '"')
                except:
                    print('#' + str(i['act_item_id']) + ' x' + str(i['quantity']))
        else:
            error.handler('ssitems', store)
        return 0
    # medals
    if args[0].lower() == 'medals' and caches.loaded is not None:
        store = ingame.get_medals(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            for i in store['awakening_items']:
                try:
                    print(
                        database.fetch(caches.acc_ver + '.db', 'awakening_items', 'id=' + str(i['awakening_item_id']))[
                            1] + ' x' + str(i['quantity']))
                except:
                    print('unknown medal x' + str(i['quantity']))
        else:
            error.handler('medals', store)
        return 0
    # name
    if args[0].lower() == 'name' and caches.loaded is not None:
        if len(args) == 2 and '' not in args:
            if len(args[1]) > 0 and len(args[1]) <= 10:
                name = str(args[1])
                store = ingame.change_name(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, name)
                if 'error' not in store:
                    print(colors.render('{success}name set as: ' + str(name)))
                else:
                    error.handler('name', store)
            else:
                print('name too long! (' + str(len(args[1])) + '/10)')
        else:
            print('no name provided.')
        return 0
    # news
    if args[0].lower() == 'news' and caches.loaded is not None:
        store = ingame.news(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            for i in store['announcements']:
                print(i['title'] + ' - ' + str(i['id']))
        else:
            error.handler('news', store)
        return 0
    # omega
    if args[0].lower() == 'omega' and caches.loaded is not None:
        farmbot.gifts()
        farmbot.missions()
        farmbot.streamline('quests')
        funcs.refresh()
        farmbot.streamline('events')
        funcs.refresh()
        farmbot.streamline('ezas')
        funcs.refresh()
        farmbot.gifts()
        farmbot.missions()
        return 0
    # potential
    if args[0].lower() == 'potential' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'dupes':
                print(colors.render('{message}checking for dupes...'))
                for i in caches.cards:
                    card = json.loads(i[3])
                    # check only for UR units
                    if str(int(i[1]) - 1) in [args[2]]:
                        # check if there's no potential to unlock
                        if len(card['unlocked_square_statuses']) != 0:
                            # check for bottom right then top right or top left then bottom left
                            if card['unlocked_square_statuses'][3] != 2:
                                # get potential board
                                card = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))
                                board_id = card[52]
                                if board_id is not None:
                                    board = database.fetchAll(caches.acc_ver + '.db', 'potential_squares',
                                                              'potential_board_id=' + str(
                                                                  board_id) + ' AND is_locked=1')
                                    for j in caches.cards:
                                        if str(j[1]) == str(int(i[1]) - 1) and str(j[0]) != str(
                                                i[0]):
                                            # unlock node on board
                                            store3 = ingame.unlock_potential_node(caches.acc_ver, caches.acc_os,
                                                                                  caches.sess_token, caches.sess_secret,
                                                                                  i[0], board[3][0], j[0], 0)
                                            if 'error' not in store3:
                                                card_ids = [store3['card']]
                                                caches.update_cards(card_ids, None)
                                                card_title = database.fetch(caches.acc_ver + '.db', 'leader_skills',
                                                                            'id=' + str(
                                                                                database.fetch(caches.acc_ver + '.db',
                                                                                               'cards',
                                                                                               'id=' + str(
                                                                                                   i[1]))[
                                                                                    22]))[1]
                                                print(colors.render('{success}Bottom right path unlocked for ' + str(
                                                    card[1]) + ' [' + card_title + ']'))
                                            else:
                                                error.handler('pnode', store3)
                                else:
                                    break
                            elif card['unlocked_square_statuses'][1] != 2:
                                # get potential board
                                card = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))
                                board_id = card[52]
                                if board_id is not None:
                                    board = database.fetchAll(caches.acc_ver + '.db', 'potential_squares',
                                                              'potential_board_id=' + str(
                                                                  board_id) + ' AND is_locked=1')
                                    for j in caches.cards:
                                        if str(j[1]) == str(int(i[1]) - 1) and str(j[0]) != str(
                                                i[0]):
                                            # unlock node on board
                                            store3 = ingame.unlock_potential_node(caches.acc_ver, caches.acc_os,
                                                                                  caches.sess_token, caches.sess_secret,
                                                                                  i[0], board[1][0], j[0], 0)
                                            if 'error' not in store3:
                                                card_ids = [store3['card']]
                                                caches.update_cards(card_ids, None)
                                                card_title = database.fetch(caches.acc_ver + '.db', 'leader_skills',
                                                                            'id=' + str(
                                                                                database.fetch(caches.acc_ver + '.db',
                                                                                               'cards', 'id=' + str(
                                                                                        i[1]))[22]))[1]
                                                print(colors.render('{success}Top right path unlocked for ' + str(
                                                    card[1]) + ' [' + card_title + ']'))
                                            else:
                                                error.handler('pnode', store3)
                                else:
                                    break
                            elif card['unlocked_square_statuses'][0] != 2:
                                # get potential board
                                card = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))
                                board_id = card[52]
                                if board_id is not None:
                                    board = database.fetchAll(caches.acc_ver + '.db', 'potential_squares',
                                                              'potential_board_id=' + str(
                                                                  board_id) + ' AND is_locked=1')
                                    for j in caches.cards:
                                        if str(j[1]) == str(int(i[1]) - 1) and str(j[0]) != str(
                                                i[0]):
                                            # unlock node on board
                                            store3 = ingame.unlock_potential_node(caches.acc_ver, caches.acc_os,
                                                                                  caches.sess_token, caches.sess_secret,
                                                                                  i[0], board[0][0], j[0], 0)
                                            if 'error' not in store3:
                                                card_ids = [store3['card']]
                                                caches.update_cards(card_ids, None)
                                                card_title = database.fetch(caches.acc_ver + '.db', 'leader_skills',
                                                                            'id=' + str(
                                                                                database.fetch(caches.acc_ver + '.db',
                                                                                               'cards', 'id=' + str(
                                                                                        i[1]))[22]))[1]
                                                print(colors.render('{success}Top left path unlocked for ' + str(
                                                    card[1]) + ' [' + card_title + ']'))
                                            else:
                                                error.handler('pnode', store3)
                                else:
                                    break
                            elif card['unlocked_square_statuses'][2] != 2:
                                # get potential board
                                card = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))
                                board_id = card[52]
                                if board_id is not None:
                                    board = database.fetchAll(caches.acc_ver + '.db', 'potential_squares',
                                                              'potential_board_id=' + str(
                                                                  board_id) + ' AND is_locked=1')
                                    for j in caches.cards:
                                        if str(j[1]) == str(int(i[1]) - 1) and str(j[0]) != str(
                                                i[0]):
                                            # unlock node on board
                                            store3 = ingame.unlock_potential_node(caches.acc_ver, caches.acc_os,
                                                                                  caches.sess_token, caches.sess_secret,
                                                                                  i[0], board[2][0], j[0], 0)
                                            if 'error' not in store3:
                                                card_ids = [store3['card']]
                                                caches.update_cards(card_ids, None)
                                                card_title = database.fetch(caches.acc_ver + '.db', 'leader_skills',
                                                                            'id=' + str(
                                                                                database.fetch(caches.acc_ver + '.db',
                                                                                               'cards', 'id=' + str(
                                                                                        i[1]))[22]))[1]
                                                print(colors.render('{success}Bottom left path unlocked for ' + str(
                                                    card[1]) + ' [' + card_title + ']'))
                                            else:
                                                error.handler('pnode', store3)
                                else:
                                    break
                            else:
                                break
        else:
            print(colors.render('{error}potential <dupes> <card id>'))
        return 0
    # sell
    if args[0].lower() == 'sell' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            if args[1] == 'quick':
                farmbot.sell_useless()
            elif args[1] == 'items':
                farmbot.sell_useless('items')
            elif len(args[1]) >= 9:
                #print('card')
                farmbot.sell_specific(args[1])
            elif len(args[1]) == 7:
                #print('item card')
                if len(args) >= 3:
                    farmbot.sell_specific(args[1], args[2])
                else:
                    print(colors.render('{error}sell <item card id> <amount>'))
        else:
            print(colors.render('{error}sell <card uid/quick/items>'))
        return 0
    # refresh
    if args[0].lower() == 'refresh' and caches.loaded is not None:
        funcs.refresh()
        return 0
    # run
    if args[0].lower() == 'run' and caches.loaded is not None:
        if len(args) == 2 and '' not in args:
            if args[1] == '1':
                # daily
                store = caches.events
                for i in store['events']:
                    if int(i['id']) == 111 or int(i['id']) == 116 or int(i['id']) == 120 or int(
                            i['id']) == 130 or int(i['id']) == 131 or int(i['id']) == 132 or int(
                        i['id']) == 134 or int(i['id']) == 135 or int(i['id']) == 177:
                        if 'quests' in i:
                            for x in i['quests']:
                                # print(str(x['id']))
                                for j in database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps',
                                                           'quest_id=' + str(x['id'])):
                                    farmbot.handler(0, str(x['id']), j[2])
                farmbot.missions()
                farmbot.gifts()
            if args[1] == '2':
                # bossrush
                is_active = False
                store = caches.events
                for i in store['events']:
                    if int(i['id']) == 701:
                        if 'quests' in i:
                            is_active = True
                            for x in i['quests']:
                                for j in database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps',
                                                           'quest_id=' + str(x['id'])):
                                    farmbot.handler(0, str(x['id']), j[2])
                if not is_active:
                    print(colors.render('{message}bossrush isn\'t available.'))
            if args[1] == '3':
                # hercule punch
                is_active = False
                store = caches.events
                for i in store['events']:
                    if int(i['id']) == 711:
                        if 'quests' in i:
                            for x in i['quests']:
                                for j in database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps',
                                                           'quest_id=' + str(x['id'])):
                                    farmbot.handler(0, str(x['id']), j[2])
                if not is_active:
                    print(colors.render('{message}hercule punch isn\'t available.'))
            if args[1] == '4':
                # sbr
                is_active = False
                store = caches.events
                for i in store['events']:
                    if int(i['id']) == 710:
                        if 'quests' in i:
                            for x in i['quests']:
                                for j in database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps',
                                                           'quest_id=' + str(x['id'])):
                                    farmbot.handler(0, str(x['id']), j[2])
                if not is_active:
                    print(colors.render('{message}SBR isn\'t available.'))
            if args[1] == '5':
                # potential
                is_active = False
                store = caches.events
                for i in store['events']:
                    if i['id'] >= 140 and i['id'] < 145:
                        try:
                            stage = \
                                database.fetch(caches.acc_ver + '.db', 'sugoroku_maps',
                                               'quest_id=' + str(i['quests'][0]['id']))[0]
                            farmbot.handler(0, str(str(stage)[0:-1]), str(stage)[-1])
                        except:
                            print('stage does not exist.')
                if not is_active:
                    print(colors.render('{message}potential isn\'t available.'))
            if args[1] == '6':
                pass
        else:
            print(colors.render('{error}run 1/2/3/4/5 ("help 2" for more.)'))
        return 0
    # stam
    if args[0].lower() == 'stam' and caches.loaded is not None:
        farmbot.restore()
        return 0
    # summon
    if args[0].lower() == 'summon' and caches.loaded is not None:
        if len(args) >= 3 and '' not in args:
            if args[2] == 's' or args[2] == 'm':
                course = None
                if args[2] == 's':
                    course = 1
                elif args[2] == 'm':
                    course = 2
                if len(args) == 4:
                    for i in range(int(args[3])):
                        farmbot.summon(args[1], course)
                        farmbot.gifts()
                else:
                    farmbot.summon(args[1], course)
                    farmbot.gifts()
            else:
                print(colors.render('{error}missing single/multi argument.'))
        elif len(args) == 2 and '' not in args:
            if args[1] == 'history':
                store = ingame.summon_history(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in store:
                    print(Fore.LIGHTYELLOW_EX + '\n==== ==== > Stone < ==== ====\n')
                    for i in store['histories']['stone']:
                        print(Fore.LIGHTYELLOW_EX + str(i['name']) + ' - ' + str(
                            i['price']) + ' Stone(s)\n' + Fore.CYAN + datetime.utcfromtimestamp(
                            int(i['drawn_at'])).strftime('%m/%d/%Y %H:%M.%S') + '\n' + Fore.WHITE + str(
                            i['card_ids']) + '\n------------------------------')
                    print(Fore.LIGHTBLUE_EX + '\n==== ==== > FP < ==== ====\n')
                    for i in store['histories']['point']:
                        print(Fore.LIGHTBLUE_EX + str(i['name']) + ' - ' + str(i[
                                                                                   'price']) + ' FP\n' + Fore.CYAN + datetime.utcfromtimestamp(
                            int(i['drawn_at'])).strftime(
                            '%m/%d/%Y %H:%M.%S') + '\n' + Fore.WHITE + str(
                            i['card_ids']) + '\n------------------------------')
                    print(Fore.LIGHTRED_EX + '\n==== ==== > Tickets < ==== ====\n')
                    for i in store['histories']['other']:
                        print(Fore.LIGHTRED_EX + str(i['name']) + ' - ' + str(i[
                                                                                  'price']) + ' Ticket(s)\n' + Fore.CYAN + datetime.utcfromtimestamp(
                            int(i['drawn_at'])).strftime(
                            '%m/%d/%Y %H:%M.%S') + '\n' + Fore.WHITE + str(
                            i['card_ids']) + '\n------------------------------')
                else:
                    error.handler('history', store)
        else:
            print(colors.render('{error}summon <ID> <s/m> / <history>'))
        return 0
    # support
    if args[0].lower() == 'leader' and caches.loaded is not None:
        if len(args) >= 2 and '' not in args:
            support_array = [int(args[1])]
            store = ingame.set_support_leader(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, support_array)
            if 'error' not in store:
                if 'support_leader_ids' in store:
                    if len(store['support_leader_ids']) != 0:
                        caches.support_leader = store['support_leader_ids'][0]
                print(colors.render('{success}Successfully set support/friend leader!'))
            else:
                error.handler('setSupport', store)
        else:
            print(colors.render('{error}support <card uid>'))
        return 0
    # team
    if args[0].lower() == 'team' and caches.loaded is not None:
        settings = funcs.get_settings()
        if len(args) >= 2 and '' not in args:
            if args[1] == 'list':
                store2 = caches.teams
                print('Current team: ' + str(store2['selected_team_num']))
                unlocked_slots = []
                already_displayed = []
                for i in store2['user_card_teams']:
                    unlocked_slots.append(int(i['num']) - 1)
                for t in store2['user_card_teams']:
                    if len(already_displayed) < len(unlocked_slots):
                        for s in unlocked_slots:
                            if int(s) not in already_displayed:
                                print(Fore.WHITE + '\n==== ==== > #' + str(int(s) + 1) + ' < ==== ====\n')
                                already_displayed.append(int(s))
                            for c in caches.cards:
                                if c[0] in store2['user_card_teams'][int(s)]['user_card_ids']:
                                    try:
                                        card = json.loads(c[3])
                                        card_text = funcs.render_card_text(card, False, True, True)
                                        print(card_text)
                                    except:
                                        print('not in database. ' + str(c[1]))
                    else:
                        break
            if args[1] == 'set':
                if len(args) >= 3:
                    store = caches.teams
                    unlocked_slots = []
                    teams = []
                    for i in store['user_card_teams']:
                        unlocked_slots.append(int(i['num']) - 1)
                        teams.append(i)
                    if int(args[2]) >= 1 and int(args[2]) <= len(unlocked_slots):
                        store2 = ingame.set_team(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, args[2], teams)
                        if 'error' not in store2:
                            print(colors.render('{success}set to deck #' + str(args[2])))
                            store = ingame.get_teams(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                            if 'error' not in store:
                                caches.teams = store
                            else:
                                error.handler('decks1', store)
                        else:
                            error.handler('teams set', store2)
                    else:
                        print(colors.render('{error}invalid team number.'))
                else:
                    print(colors.render('{error}no deck number provided.'))
            if args[1] == 'build':
                if len(args) >= 3:
                    if args[2] != 'mono' and args[2] != 'rainbow' and args[2] != 'cat':
                        cards = []
                        if ',' in str(args[2]):
                            spl = str(args[2]).split(',')
                            for i in spl:
                                cards.append(int(i))
                        else:
                            cards.append(int(args[2]))
                        if len(cards) != 0:
                            if len(cards) <= 6:
                                while len(cards) < 6:
                                    cards.append(0)
                            decks = caches.teams
                            decks['user_card_teams'].remove(decks['user_card_teams'][0])
                            new_decks = [{'num': 1, 'user_card_ids': cards}]
                            for i in decks:
                                new_decks.append(i)
                            if settings['dev_mode']:
                                print(new_decks[0])
                            store = ingame.set_team(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                   '1', new_decks)
                            if 'error' not in store:
                                caches.teams = store
                                print(colors.render('{success}Team built - deck #1'))
                            else:
                                error.handler('tb set2', store)
                        else:
                            print(colors.render('{error}team can\'t be blank!'))
                else:
                    print(colors.render('{error}team build <card uid, uid, uid>'))
        else:
            print(colors.render('{error}team <list/set/build>'))
        return 0
    # toggle
    if args[0].lower() == 'toggle' and caches.loaded is not None:
        if len(args) == 2:
            if args[1] == 'stone':
                settings = funcs.get_settings()
                settings['stam_use_stone'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Stone usage: ' + str(settings['stam_use_stone'])))
            if args[1] == 'tb':
                settings = funcs.get_settings()
                settings['team_builder'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Team builder: ' + str(settings['team_builder'])))
            if args[1] == 'cap':
                settings = funcs.get_settings()
                settings['capacity'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Auto increase box size: ' + str(settings['capacity'])))
            if args[1] == 'drops':
                settings = funcs.get_settings()
                settings['display_drops'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Drops: ' + str(settings['display_drops'])))
            if args[1] == 'ids':
                settings = funcs.get_settings()
                settings['display_ids'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Card IDs: ' + str(settings['display_ids'])))
            if args[1] == 'cards':
                settings = funcs.get_settings()
                settings['display_only_ids'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Only card IDs: ' + str(settings['display_only_ids'])))
            if args[1] == 'names':
                settings = funcs.get_settings()
                settings['display_stage_names'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Stage names: ' + str(settings['display_stage_names'])))
            if args[1] == 'bonus':
                settings = funcs.get_settings()
                settings['drop_bonus'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Drops bonus: ' + str(settings['drop_bonus'])))
            if args[1] == 'meat':
                settings = funcs.get_settings()
                settings['stam_use_item'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Stamina item usage: ' + str(settings['stam_use_item'])))
            if args[1] == 'gifts':
                settings = funcs.get_settings()
                settings['display_claimed_gifts'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Claimed gift list: ' + str(settings['display_claimed_gifts'])))
            if args[1] == 'missions':
                settings = funcs.get_settings()
                settings['display_claimed_missions'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Claimed mission list: ' + str(settings['display_claimed_missions'])))
            if args[1] == 'dropnames':
                settings = funcs.get_settings()
                settings['display_drop_names'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Drop names: ' + str(settings['display_drop_names'])))
            if args[1] == 'stack':
                settings = funcs.get_settings()
                settings['stack_drops'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Stack drops: ' + str(settings['stack_drops'])))
            if args[1] == 'animation':
                settings = funcs.get_settings()
                settings['animations'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Output summon animations: ' + str(settings['animations'])))
            if args[1] == 'keys':
                settings = funcs.get_settings()
                settings['use_keys'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Use keys: ' + str(settings['use_keys'])))
            if args[1] == 'potential':
                settings = funcs.get_settings()
                settings['potential_node'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Unlock paths after summon: ' + str(settings['potential_node'])))
            if args[1] == 'hourglass':
                settings = funcs.get_settings()
                settings['hourglass'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Use hourglass for Potential: ' + str(settings['hourglass'])))
            if args[1] == 'baba':
                settings = funcs.get_settings()
                settings['baba_useless'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Baba useless R & SR: ' + str(settings['baba_useless'])))
            if args[1] == 'autosell':
                settings = funcs.get_settings()
                settings['autosell'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Autosell after max box: ' + str(settings['autosell'])))
            if args[1] == 'sellsummon':
                settings = funcs.get_settings()
                settings['summon_sell'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Autosell after summon: ' + str(settings['summon_sell'])))
            if args[1] == 'dev':
                settings = funcs.get_settings()
                settings['dev_mode'] ^= True
                funcs.save_settings(settings)
                print(colors.render('{success}Developer: ' + str(settings['dev_mode'])))
        else:
            print(colors.render('{error}toggle <stone/tb>'))
        return 0
    # train
    if args[0].lower() == 'train' and caches.loaded is not None:
        if len(args) == 3:
            if ',' in str(args[2]):
                cards = []
                spl = str(args[2]).split(',')
                for i in spl:
                    cards.append(int(i))
            else:
                cards = [int(args[2])]
            item_cards = []
            for i in caches.item_cards:
                if i[0] in cards:
                    cards.remove(i)
                    one_card = {'card_id': i[1], 'quantity': 1}
                    item_cards.remove(one_card)
                    one_card['quantity'] = int(one_card['quantity']) + 1
                    item_cards.append(one_card)
                else:
                    item_cards.append({'card_id': i[1], 'quantity': 1})
            items = []
            store = ingame.train_card(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, args[1], cards, 1, items, item_cards)
            if 'error' not in store:
                card_ids = [store['card']]
                caches.update_cards(card_ids, None)
                # remove dupes from box
                card_ids = []
                for i in cards:
                    card_ids.append({'id': i})
                caches.remove_cards(card_ids, item_cards)
                print(colors.render('{success}S U C C E S S !'))
                # {'card': {'id': 1289887601, 'card_id': 1000800, 'exp': 763, 'skill_lv': 4, 'is_favorite': False, 'awakening_route_id': None, 'is_released_potential': False, 'released_rate': 0.0, 'optimal_awakening_step': None, 'card_decoration_id': None, 'awakenings': [], 'unlocked_square_statuses': [], 'updated_at': 1607352116, 'created_at': 1606168106, 'potential_parameters': [], 'equipment_skill_items': [], 'link_skill_lvs': []}
            else:
                error.handler('train', store)
        else:
            print(colors.render('{error}train <card uid> <card uid,card uid,card uid>'))
        return 0
    # wallpaper
    if args[0].lower() == 'wallpaper' and caches.loaded is not None:
        if len(args) >= 2:
            if args[1] == 'list':
                store = ingame.get_items(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in store:
                    for i in store['wallpaper_items']:
                        try:
                            wallpaper = database.fetch(caches.acc_ver + '.db', 'wallpaper_items',
                                                       'id=' + str(i['wallpaper_item_id']))
                            name = wallpaper[1]
                            if wallpaper[2] is not None:
                                desc = wallpaper[2]
                            else:
                                desc = ''
                        except:
                            name = 'Wallpaper not in database.'
                            desc = ''
                        print(colors.render(
                            '{message}#' + str(i['wallpaper_item_id']) + ' - ' + str(name) + '\n{success}' + str(desc)))
                else:
                    error.handler('Wallpapers', store)
            if args[1] == 'set':
                if len(args) == 3:
                    store = ingame.set_wallpaper(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                args[2])
                    if 'error' not in store:
                        wallname = database.fetch(caches.acc_ver + '.db', 'wallpaper_items', 'id=' + str(args[2]))
                        if wallname is not None:
                            print(colors.render('{success}set as: ' + str(args[2]) + ' - ' + str(wallname[1])))
                        else:
                            print(colors.render('{success}set as: ' + str(args[2])))
                    else:
                        error.handler('wallpaper', store)
                else:
                    print(colors.render('{error}missing wallpaper ID.'))
        else:
            print(colors.render('{error}wallpaper <list/set>'))
        return 0



    # developer commands
    # limits
    if args[0].lower() == 'limits' and caches.loaded is not None:
        f = open('../stage_limits.txt', 'w')
        added = []
        events = caches.events
        for event in events['events']:
            for i in event['quests']:
                if 'limitations' in i and len(i['limitations']) != 0:
                    if int(event['id']) not in added:
                        added.append(int(event['id']))
                        f.write('Area #' + str(event['id']) + '------------\n')
                        print(str(event['id']))
                    f.write(str(i['limitations']) + '\n')
        f.close()
        added = []
        return 0
    # api
    if args[0].lower() == 'api':
        if len(args) == 2 and '' not in args:
            if args[1] == 'gb' or args[1] == 'jp':
                store = outgame.ping(args[1])
                print(colors.render('{success}Host: ' + store['ping_info']['host'] + '\nPort: ' + str(
                    store['ping_info']['port']) + '\nAPI port: ' + str(
                    store['ping_info']['port_str']) + '\nCF URI Prefix: ' + store['ping_info']['cf_uri_prefix']))
            else:
                print(colors.render('{error}invalid version input.'))
        else:
            print(colors.render('{error}api gb/jp'))
        return 0
    # wallpapers
    if args[0].lower() == 'wallpapers' and caches.loaded is not None:
        f = open('../wallpapers.txt', 'w')
        d = database.fetchAll(caches.acc_ver + '.db', 'wallpaper_items', None)
        if d is not None and len(d) != 0:
            for i in d:
                f.write('#' + str(i[0]) + ' - ' + str(i[1]) + '\n' + i[2])
        else:
            print(colors.render('{error}no wallpapers in database!'))
        return 0
    # db
    if args[0].lower() == 'db' and caches.loaded is not None:
        if len(args) == 2 and '' not in args:
            if args[1] == 'gb' or args[1] == 'jp':
                if fs.path.isfile('data/' + args[1] + '-data.txt'):
                    f = open('data/' + args[1] + '-data.txt', 'r')
                    print(f.read())
                    f.close()
                else:
                    print(colors.render('{error}no database downloaded.'))
            else:
                print(colors.render('{error}invalid version input.'))
        else:
            print(colors.render('{error}db gb/jp'))
        return 0
    # code to test
    if args[0].lower() == 'test' and caches.loaded is not None:
        store = ingame.card_updates(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, args[1])
        print(store)
