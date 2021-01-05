import requests
import json
import os as fs
import re
from colorama import init, Fore
from datetime import datetime
import config as config
import utils.crypto as crypto
import utils.error as error
import utils.database as database
import api.auth as auth
import api.caches as caches
import api.outgame as outgame
import utils.colors as colors
init(autoreset=True)

def save_settings(data):
    f = open('../settings-2.0.6.json', 'w')
    f.write(json.dumps(data))
    f.close()
    return True

def get_settings():
    f = open('../settings-2.0.6.json', 'r')
    txt = f
    settings = json.load(txt)
    f.close()
    return settings

def subfolders():
    if not fs.path.isdir('../saves'):
        try:
            fs.mkdir('../saves')  # outside source
            print('"saves" directory created.')
        except:
            print('unable to create "saves" directory.')
    if not fs.path.isdir('../summaries'):
        try:
            fs.mkdir('../summaries')  # outside source
        except:
            print('unable to create "summaries" directory.')
    if not fs.path.isdir('./data'):
        try:
            fs.mkdir('./data')  # inside source
        except:
            print('unable to create "data" directory.')
    if not fs.path.isdir('./boxes'):
        try:
            fs.mkdir('./boxes')  # inside source
        except:
            print('unable to create "boxes" directory.')
    if fs.path.isfile('../settings-2.0.5.2.json'):
        fs.unlink('../settings-2.0.5.2.json')
    if not fs.path.isfile('../settings-2.0.6.json'):
        settings = {
            'stam_use_stone': True,
            'team_builder': False,
            'capacity': True,
            'display_drops': True,
            'display_ids': True,
            'display_only_ids': False,
            'display_stage_names': True,
            'drop_bonus': False,
            'potential_node': False,
            'stam_use_item': False,
            'display_claimed_gifts': False,
            'display_claimed_missions': False,
            'display_drop_names': True,
            'stack_drops': True,
            'drops_boost': False,
            'animations': False,
            'use_keys': False,
            'hourglass': False,
            'baba_useless': False,
            'autosell': True,
            'summon_sell': False,
            'dev_mode': False,
            'colors': {
                'command': 'yellow',
                'description': 'green',
                'error': 'red',
                'success': 'green',
                'message': 'yellow',
                'drops': 'cyan'
            }
        }
        save_settings(settings)


def check_servers(ver):
    try:
        if ver == 'gb':
            url = config.gb_url + '/ping'
            code = config.gb_code['android']
        else:
            url = config.jp_url + '/ping'
            code = config.jp_code['android']
        headers = {
            'X-Platform': 'android',
            'X-ClientVersion': code,
            'X-Language': 'en',
            'X-UserID': '////'
        }
        r = requests.get(url, data=None, headers=headers)
        store = r.json()
        if 'error' not in store:
            if 'ping_info' in store:
                url = store['ping_info']['host']
                port = store['ping_info']['port_str']
                if ver == 'gb':
                    config.gb_url = 'https://' + str(url)
                    config.gb_port = str(port)
                else:
                    config.jp_url = 'https://' + str(url)
                    config.jp_port = str(port)
                return True
            else:
                print(colors.render('{error}[' + ver + ' server] can\'t connect.'))
        else:
            if 'title' in store['error']:
                if 'description' in store['error'] and store['error']['description'] != '':
                    desc = str(store['error']['description']) + '\n' + str(store['error']['code'])
                else:
                    desc = str(store['error']['code'])
                if 'until' in store['error'] and store['error']['until'] != '':
                    ends_at = '\nEnds: ' + datetime.utcfromtimestamp(int(store['error']['until'])).strftime('%m/%d/%Y %H:%M.%S')
                else:
                    ends_at = ''
                print(colors.render('{error}[' + str(ver).upper() + '] ' + store['error']['title'] + '\n' + desc + ends_at))
                if ver == 'gb':
                    config.gb_maint = True
                else:
                    config.jp_maint = True
            else:
                print(colors.render('{error}[' + ver + ' server] can\'t connect.'))
            return True
    except:
        print(colors.render('{error}[' + ver + ' server] can\'t connect.'))
        return False


def navigator(page):
    f = open(f"./farming/navi/{page}", 'r')
    txt = f.read().replace('{CYAN}', Fore.CYAN).replace('{LTYELLOW}', Fore.LIGHTYELLOW_EX).replace('{GREEN}', Fore.LIGHTGREEN_EX).replace('{YELLOW}', Fore.YELLOW).replace('{RED}', Fore.LIGHTRED_EX).replace('{BLUE}', Fore.BLUE).replace('{PURPLE}', Fore.LIGHTMAGENTA_EX).replace('\\n', '\n')
    for match in re.findall(r'\\x[0-9A-Fa-f]{2}', txt):
        txt = txt.replace(match, chr(int(match[2:], 16)))
    f.close()
    print(colors.render(txt))


def check_database(ver, os, token, secret):
    print(colors.render('{message}checking for new database...'))
    store = outgame.getDatabase(ver, os, token, secret)
    if 'error' not in store:
        version = store['version']
        caches.database_ts = str(version)
        if fs.path.isfile('./data/' + caches.acc_ver + '-data.txt'):
            f = open('./data/' + caches.acc_ver + '-data.txt', 'r')
            ver2 = f.readline().rstrip()
            f.close()
            if str(ver2) != str(version):
                print(str(version))
                fs.unlink('./data/' + caches.acc_ver + '-data.txt')
                database.download(ver, os, token, secret, version, store['url'])
        else:
            print(str(version))
            database.download(ver, os, token, secret, version, store['url'])
        return True
    else:
        error.handler('DB DL', store)
        return False


def check_asset():
    print(colors.render('{message}checking for new asset(s)...'))
    if fs.path.isfile('./data/' + caches.acc_ver + '-dl.txt'):
        f = open('./data/' + caches.acc_ver + '-dl.txt', 'r')
        ver2 = f.readline().rstrip()
        f.close()
        store = outgame.getAsset(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, ver2)
        if 'error' not in store:
            version = store['latest_version']
            if str(ver2) != str(version):
                print(str(version))
                fs.unlink('./data/' + caches.acc_ver + '-dl.txt')
                f = open('./data/' + caches.acc_ver + '-dl.txt', 'w')
                f.write(str(version) + '\n')
                f.close()
                caches.asset_ts = str(version)
            else:
                caches.asset_ts = str(version)
        else:
            error.handler('checkAsset', store)
    else:
        store = outgame.getAsset(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            version = store['latest_version']
            print(str(version))
            f = open('./data/' + caches.acc_ver + '-dl.txt', 'w')
            f.write(str(version) + '\n')
            f.close()
            caches.asset_ts = str(version)
        else:
            error.handler('checkAsset', store)


def create_save_file(acc_ver, acc_os, iden):
    print(colors.render('{success}What would you like to name this save?'))
    save = input().lower()
    if len(str(save)) >= 1:
        if fs.path.isfile('../saves/' + str(save) + '.txt'):
            print(colors.render('{error}save name already exists!'))
            create_save_file(acc_ver, acc_os, iden)
        else:
            if ' ' not in save and '\n' not in save:
                f = open('../saves/' + str(save) + '.txt', 'w')
                f.write(acc_ver + ':' + acc_os + '\n')
                f.write(str(iden.replace('\n', '')) + '\n')
                f.close()
                print(colors.render('{success}saved account as "saves/' + str(save) + '.txt"\nuse "load ' + str(save) + '" to log-in anytime.'))
                return save
            else:
                print(colors.render('{error}save name must not contain spaces!'))
                create_save_file(acc_ver, acc_os, iden)
    else:
        print(colors.render('{error}save name is too small!'))
        create_save_file(acc_ver, acc_os, iden)


def refresh():
    #save = caches.loaded
    store = auth.login(caches.acc_ver, caches.acc_os, crypto.basic(caches.account), False)
    if 'error' not in store:
        caches.sess_token, caches.sess_secret = store['access_token'], store['secret']
        print(colors.render('{success}session renewed.'))
    else:
        error.handler('refresh', store)

def render_card_text(card, is_drop, add_rarity, all_info, is_friend=False):
    settings = get_settings()
    '''
    rarity changed from 6 to 5
    elemental changed from 13 to 12
    leader skill changed from 24 to 22
    max sa changed from 15 to 14
    max lvl changed from 14 to 13
    team cost changed from 5 to 4
    potential board changed from 54 to 52

    TODO get closest lvl to EXP value
    database.fetch(caches.acc_ver + '.db', 'card_exps', 'exp_total=' + str(i['exp'])))[1]
    '''
    card_quantity = ''
    id_toggle = ''
    if is_drop:
        if 'item_id' in card:
            card_id = str(card['item_id'])
        else:
            card_id = str(card['card_id'])
        card_quantity = 'x' + str(card['quantity'])
    elif is_friend:
        card = card['user']['leader']
        card_id = str(card['card_id'])
    else:
        card_id = str(card['card_id'])
    if settings['display_ids']:
        id_toggle = ' (' + card_id + ')'
    element = '?'
    db_ele = database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[12]
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
    if add_rarity:
        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[5] is 0:
            rarity = 'N'
        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[5] is 1:
            rarity = 'R'
        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[5] is 2:
            rarity = 'SR'
        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[5] is 3:
            rarity = 'SSR'
        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[5] is 4:
            rarity = 'UR'
        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[5] is 5:
            rarity = 'LR'
        element = element + ' ' + rarity
    if all_info:
        card = element + ' ' + database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(card['card_id']))[
            1] + ' [' + database.fetch(caches.acc_ver + '.db', 'leader_skills', 'id=' + str(
            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(card['card_id']))[22]))[
            1] + '] (' + str(card['card_id']) + ')\n' + Fore.LIGHTWHITE_EX + 'SA: ' + str(card['skill_lv']) + '/' + str(
            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(card['card_id']))[
                14]) + ', Potential: ' + str(card['released_rate']) + '%, Lvl: ?/' + str(
            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(card['card_id']))[
                13]) + ', Cost: ' + str(
            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(card['card_id']))[
                4]) + ', uid: ' + str(card['id'])
    else:
        card = element + ' ' + database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[
            1] + ' [' + database.fetch(caches.acc_ver + '.db', 'leader_skills', 'id=' + str(
            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + card_id)[22]))[
                   1] + '] ' + card_quantity + id_toggle
    return card
