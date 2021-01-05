'''
fapro.py is functions for farming/farmbot processes without cluttering up commands.py
some processes require extensive handling of API errors etc.
'''
import requests
import json
import random
import time

import config as config
import utils.crypto as crypto
import utils.error as error
import utils.database as database
import api.caches as caches
import api.ingame as ingame
import utils.funcs as funcs
import utils.colors as colors
import farming.autoteam as autoteam

failed_sell_attempts = 0
names = ['Abra', 'Armadillo', 'Beat', 'Berserker', 'Erito', 'Forte', 'Froze', 'Kabra', 'Kagyu', 'Mirego', 'Mizore', 'Nico', 'Nimu', 'Note', 'Pokoh', 'Rezok', 'Salaga', 'Tsumuri', 'Viola']


# tutorial
def tutorial(ver, os, token, secret, iden):
    global names
    if os == 'android':
        dua = caches.device_agent1
    else:
        dua = caches.device_agent2
    if ver == 'gb':
        code = config.gb_code[str(os)]
    else:
        code = config.jp_code[str(os)]
    if ver == 'gb':
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 10}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 20}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 30}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.gb_url + '/tutorial/gasha'
        auth = crypto.mac(ver, token, secret, 'POST', '/tutorial/gasha')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print(colors.render('{success}Tutorial 1/7 - Summon'))
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 40}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.gb_url + '/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        name = random.randint(0, len(names) - 1)
        data = {'user': {'name': names[name]}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 2/7 - Set name as "' + str(names[name]) + '"'))
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 50}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 60}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 70}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 77}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 3/7 - Dragonball #3 / Defeat hercule'))
        #######################
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 80}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.gb_url + '/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'user': {'is_ondemand': True}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 4/7 - Update user'))
        #######################
        url = config.gb_url + '/tutorial/finish'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial/finish')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        requests.put(url, data=None, headers=headers)
        print(colors.render('{success}Tutorial 5/7 - Finish battle'))
        #######################
        url = config.gb_url + '/missions/put_forward'
        auth = crypto.mac(ver, token, secret, 'POST', '/missions/put_forward')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print(colors.render('{success}Tutorial 6/7 - Update missions'))
        #######################
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 90}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.gb_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 999}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 7/7 - Tutorial complete'))
        #######################
        url = config.gb_url + '/apologies/accept'
        auth = crypto.mac(ver, token, secret, 'PUT', '/apologies/accept')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.put(url, data=None, headers=headers)
        #######################
        save = funcs.create_save_file(ver, os, iden)
        caches.load_account(save, iden, ver, os, token, secret, True)
    else:
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 10}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 20}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 30}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.jp_url + '/tutorial/gasha'
        auth = crypto.mac(ver, token, secret, 'POST', '/tutorial/gasha')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print(colors.render('{success}Tutorial 1/7 - Summon'))
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 40}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.jp_url + '/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        name = random.randint(0, len(names) - 1)
        data = {'user': {'name': names[name]}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 2/7 - Set name as "' + str(names[name]) + '"'))
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 50}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 60}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 70}
        requests.put(url, data=json.dumps(data), headers=headers)
        #######################
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 77}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 3/7 - Dragonball #3 / Defeat hercule'))
        #######################
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 80}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.jp_url + '/user'
        auth = crypto.mac(ver, token, secret, 'PUT', '/user')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'user': {'is_ondemand': True}}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 4/7 - Update user'))
        #######################
        url = config.jp_url + '/tutorial/finish'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial/finish')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        requests.put(url, data=None, headers=headers)
        print(colors.render('{success}Tutorial 5/7 - Finish battle'))
        #######################
        url = config.jp_url + '/missions/put_forward'
        auth = crypto.mac(ver, token, secret, 'POST', '/missions/put_forward')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.post(url, data=None, headers=headers)
        print(colors.render('{success}Tutorial 6/7 - Update missions'))
        #######################
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 90}
        requests.put(url, data=json.dumps(data), headers=headers)
        url = config.jp_url + '/tutorial'
        auth = crypto.mac(ver, token, secret, 'PUT', '/tutorial')
        headers = {'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua}
        data = {'progress': 999}
        requests.put(url, data=json.dumps(data), headers=headers)
        print(colors.render('{success}Tutorial 7/7 - Tutorial complete'))
        #######################
        url = config.jp_url + '/apologies/accept'
        auth = crypto.mac(ver, token, secret, 'PUT', '/apologies/accept')
        headers = { 'X-Platform': os, 'X-ClientVersion': code, 'X-AssetVersion': '////', 'X-DatabaseVersion': '////', 'Content-Type': 'application/json', 'Accept': '*/*', 'Authorization': auth, 'User-Agent': dua }
        requests.put(url, data=None, headers=headers)
        #######################
        save = funcs.create_save_file(ver, os, iden)
        caches.load_account(save, iden, ver, os, token, secret, True)
    # print(colors.render('{message}type "help" for a list of commands.')


# card selling
def sell_specific(unique_card, quantity=None):
    #print(f"{unique_card}-{quantity}")
    card_ids = []
    item_ids = []
    card_objs = []
    item_objs = []
    if quantity is None:
        quantity = 1
    for i in caches.cards:
        card_ids.append(i[0])
    if int(unique_card) in card_ids:
        #print('card')
        card_objs = [{'id': int(unique_card)}]
    for i in caches.item_cards:
        item_ids.append(i[0])
    if int(unique_card) in item_ids:
        #print('item card')
        item_objs.append({'card_id': int(unique_card), 'quantity': int(quantity)})
    store = ingame.sell_card(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, card_objs, item_objs)
    if 'error' not in store:
        caches.remove_cards(card_objs, item_objs)
        print(colors.render('{success}sold ' + str(len(card_objs)) + ' cards & ' + str(len(item_objs)) + ' item cards!'))
        return True
    else:
        error.handler('sold', store)
        return False


def sell_useless(which=None):
    global failed_sell_attempts
    settings = funcs.get_settings()
    if failed_sell_attempts > 0:
        if settings['capacity']:
            ingame.capacity(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            print(colors.render('{success}increased box capacity by 5+'))
            failed_sell_attempts = 0
            return True
        else:
            failed_sell_attempts = 0
            return False
    else:
        print(colors.render('{message}gathering cards to sell...'))
        cards_on_teams = []
        for x in caches.teams['user_card_teams']:
            for j in x['user_card_ids']:
                cards_on_teams.append(str(j))
        card_ids = []
        card_objs = []
        item_objs = []
        selling_count = 0
        if which == 'items':
            for i in caches.item_cards:
                # hercule statues
                statues = ['1002630', '1002640', '1002650', '1005480', '1011480', '1011481']
                if str(i[0]) in statues:
                    if selling_count + int(i[1]) < 99:
                        item_objs.append({'card_id': i[0], 'quantity': i[1]})
                        selling_count = selling_count + int(i[1])
        else:
            for i in database.query(f"./boxes/{caches.loaded}.db", 'drops', None, 1):
                if selling_count <= 98 and str(i[0]) not in cards_on_teams and str(i[0]) != str(
                        caches.support_leader):
                    # all N
                    if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 0:
                        card_ids.append(i[0])
                        card_objs.append({'id': [0]})
                        selling_count = selling_count + 1
                    # all R
                    if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 1:
                        card_ids.append(i[0])
                        card_objs.append({'id': [0]})
                        selling_count = selling_count + 1
                    '''try:
                        
                    except:
                        print('does the database exist?')
                        break'''
            if len(card_ids) == 0:
                for i in database.query(f"./boxes/{caches.loaded}.db", 'cards', None, 1):
                    if database.query(f"./boxes/{caches.loaded}.db", 'cards', 'id=' + str(i[0]),
                                      0) is not None or database.query(f"./boxes/{caches.loaded}.db", 'drops',
                                                                       'unique_id=' + str(i[0]), 0) is not None:
                        card = json.loads(i[3])
                        if selling_count <= 98 and str(i[0]) not in cards_on_teams and not card['is_favorite'] and str(
                                i[0]) != str(caches.support_leader):
                            try:
                                # all N
                                if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 0:
                                    card_ids.append(i[0])
                                    card_objs.append(card)
                                    selling_count = selling_count + 1
                                # all R
                                if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 1:
                                    card_ids.append(i[0])
                                    card_objs.append(card)
                                    selling_count = selling_count + 1
                            except:
                                print('does the database exist?')
                                break
        if len(card_ids) != 0 or len(item_objs) != 0:
            store = ingame.sell_card(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, card_ids, item_objs)
            if 'error' not in store:
                print(colors.render('{success}sold ' + str(len(card_ids)) + ' cards & ' + str(len(item_objs)) + ' item cards!'))
                failed_sell_attempts = 0
                caches.remove_cards(card_objs, item_objs)
                return True
            else:
                error.handler('sold1', store)
                failed_sell_attempts = failed_sell_attempts + 1
                return False
        else:
            print(len(database.query(f"./boxes/{caches.loaded}.db", 'drops', None, 1)))
            print(len(database.query(f"./boxes/{caches.loaded}.db", 'cards', None, 1)))
            print(colors.render('{error}no cards/items to sell.'))
            return False


def baba_specific(card, quantity=1):
    card_ids = []
    card_objs = []
    item_objs = []
    for i in caches.cards:
        if str(i[0]) == str(card):
            card_ids = [int(card)]
            card_objs = [{'id': card}]
    for i in caches.item_cards:
        if str(i[1]) == str(card):
            item_objs = [{'card_id': card, 'quantity': quantity}]
    store = ingame.baba_sell(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, 'cards', card_ids, item_cards=item_objs)
    if 'error' not in store:
        print(colors.render('{success}exchanged ' + str(len(card_ids)) + ' cards & ' + str(len(item_objs)) + ' item cards!'))
        caches.remove_cards(card_objs, item_objs)
        return True
    else:
        error.handler('bsold1', store)
        return False


def baba_useless():
    global failed_sell_attempts
    print(colors.render('{message}gathering cards to baba...'))
    store2 = caches.teams
    teams = []
    for x in store2['user_card_teams']:
        for j in x['user_card_ids']:
            teams.append(j)
    card_ids = []
    card_objs = []
    item_objs = []
    selling_count = 0
    statues = config.x0a4_0
    for i in database.query(f"./boxes/{caches.loaded}.db", 'drops', None, 1):
        if selling_count <= 98 and str(i[0]) not in teams and str(i[0]) != str(caches.support_leader):
            try:
                # all R
                if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 1:
                    card_ids.append(i[0])
                    card_objs.append({'id':[0]})
                    selling_count = selling_count + 1
                # all SR
                if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 2:
                    card_ids.append(i[0])
                    card_objs.append({'id':[0]})
                    selling_count = selling_count + 1
            except:
                print('does the database exist?')
                break
    if len(card_ids) == 0:
        for i in database.query(f"./boxes/{caches.loaded}.db", 'cards', None, 1):
            if database.query(f"./boxes/{caches.loaded}.db", 'cards', 'id=' + str(i[0]),
                              0) is not None or database.query(f"./boxes/{caches.loaded}.db", 'drops',
                                                               'unique_id=' + str(i[0]), 0) is not None:
                card = json.loads(i[3])
                if selling_count <= 98 and i[0] not in teams and not card['is_favorite'] and str(
                        i[1]) not in config.x0a2_0 and str(int(i[1]) + 1) not in config.x0a2_0 and str(i[1]) != str(
                        caches.support_leader):
                    try:
                        # all R
                        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 1:
                            card_ids.append(i[0])
                            card_objs.append(card)
                            selling_count = selling_count + 1
                        # all SR
                        if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] is 2:
                            card_ids.append(i[0])
                            card_objs.append(card)
                            selling_count = selling_count + 1
                    except:
                        print('does the database exist?')
                        break
    for i in caches.item_cards:
        if selling_count + int(i[1]) < 99 and str(i[0]) not in config.x0a2_0 and str(int(i[0]) + 1) not in config.x0a2_0 and str(i[0]) not in statues:
            try:
                if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[0])) != None:
                    # all R
                    if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[0]))[5] is 1:
                        item_objs.append({'card_id': i[0], 'quantity': int(i[1])})
                        selling_count = selling_count + int(i[1])
                    # all SR
                    if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[0]))[5] is 2:
                        item_objs.append({'card_id': i[0], 'quantity': int(i[1])})
                        selling_count = selling_count + int(i[1])
                else:
                    print('card not in database.')
            except:
                print('does the database exist?')
                break
    if len(card_ids) != 0 or len(item_objs) != 0:
        store = ingame.baba_sell(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, 'cards', card_ids, item_cards=item_objs)
        if 'error' not in store:
            print(colors.render('{success}exchanged ' + str(len(card_ids)) + ' cards & ' + str(len(item_objs)) + ' item cards!'))
            caches.remove_cards(card_objs, item_objs)
        else:
            error.handler('bsold1', store)
            failed_sell_attempts = failed_sell_attempts + 1
    else:
        if failed_sell_attempts > 0:
            ingame.capacity(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            print(colors.render('{success}increased box capacity by 5+'))
            failed_sell_attempts = 0
        else:
            print(colors.render('{error}no cards to baba.'))


# gift accept
def gifts():
    settings = funcs.get_settings()
    print(colors.render('{message}apologies/comeback/hercule gifts...'))
    store = ingame.home_resources(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
    if 'error' not in store:
        presents = []
        # TODO comeback
        # hercule
        if len(store['random_login_bonuses']) != 0:
            for i in store['random_login_bonuses']:
                if 'random_login_bonus' in i and 'token' in i:
                    store = ingame.claim_random_login(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, i['random_login_bonus']['elapsed_days'], i['expire'], i['random_login_bonus']['id'], i['token'])
                    if 'error' not in store:
                        if 'cards' in store['user_items']:
                            card_ids = store['user_items']['cards']
                        else:
                            card_ids = None
                        if 'item_cards' in store['user_items']:
                            item_cards = store['user_items']['item_cards']
                        else:
                            item_cards = None
                        caches.add_cards(card_ids, item_cards)
                        print(colors.render('{success}\"' + str(i['announcement']['title']) + '\" claimed!'))
                    else:
                        error.handler('randomClaim', store)
                else:
                    print(colors.render('{error}no bonus or token.'))
        else:
            print(colors.render('{error}None to claim.'))
        # TODO apologies
    else:
        error.handler('gift2', store)
    print(colors.render('{message}cumulative/consecutive/celebration gifts...'))
    store = ingame.gifts(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
    if 'error' not in store:
        store2 = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
        if 'error' not in store2:
            presents = []
            user = store2['user']
            box = str(len(caches.cards))
            if int(box) >= int(user['total_card_capacity']):
                print(colors.render('{error}Can\'t accept cards your box is full!\nuse "gift" again when it isn\'t.'))
                for i in store['gifts']:
                    if i['item_type'] != 'Card':
                        presents.append(i['id'])
                        if settings['display_claimed_gifts']:
                            print(colors.render(
                                '{drops}' + str(i['item_type']) + ' x' + str(i['quantity']) + '\n' + str(
                                    i['description'])))
            else:
                for i in store['gifts']:
                    presents.append(i['id'])
                    if settings['display_claimed_gifts']:
                        print(colors.render(
                            '{drops}' + str(i['item_type']) + ' x' + str(i['quantity']) + '\n' + str(i['description'])))
            if len(presents) != 0:
                store4 = ingame.accept_gifts(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, presents)
                if 'error' not in store4:
                    #print(store4)
                    if 'cards' in store4['user_items']:
                        card_ids = store4['user_items']['cards']
                    else:
                        card_ids = None
                    if 'item_cards' in store4['user_items']:
                        item_cards = store4['user_items']['item_cards']
                    else:
                        item_cards = None
                    caches.add_cards(card_ids, item_cards)
                    # {'gifts': [{'id': 1685078138, 'item': {'item_id': 1009850, 'item_type': 'Card', 'card_exp_init': 0, 'quantity': 1}, 'result': 'success'},
                    # 'user_items': {'item_cards': [{'id': 9117945, 'card_id': 1009850, 'quantity': 1}
                    print(colors.render('{success}accepted ' + str(len(presents)) + ' gifts.'))
                else:
                    error.handler('gAccept', store4)
            else:
                print(colors.render('{error}No gifts to accept.'))
        else:
            error.handler('gUsr1', store2)
    else:
        error.handler('giftLS', store)


# mission claim
def missions():
    settings = funcs.get_settings()
    store = ingame.missions(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
    if 'error' not in store:
        missions = []
        db_ids = []
        accepted = []
        for i in store['missions']:
            if i['completed_at'] is not None and i['accepted_reward_at'] is None:
                missions.append(i['id'])
                if settings['display_claimed_missions']:
                    try:
                        print(colors.render('{drops}' + database.fetch(caches.acc_ver + '.db', 'missions', 'id=' + str(i['mission_id']))[3] + '\n' + database.fetch(caches.acc_ver + '.db', 'mission_rewards', 'id=' + str(i['mission_id']))[3] + ' x' + str(database.fetch(caches.acc_ver + '.db', 'mission_rewards', 'id=' + str(i['mission_id']))[4])))
                    except:
                        print(colors.render('{drops}unknown ID: ' + str(i['mission_id'])))
        if len(missions) != 0:
            store2 = ingame.accept_missions(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, missions)
            if 'error' not in store2:
                #print(store2)
                if 'cards' in store2['user_items']:
                    card_ids = store2['user_items']['cards']
                else:
                    card_ids = None
                if 'item_cards' in store2['user_items']:
                    item_cards = store2['user_items']['item_cards']
                else:
                    item_cards = None
                caches.add_cards(card_ids, item_cards)
                # 'mission_rewards': [{'item_id': 1002640, 'item_type': 'Card', 'card_exp_init': 93879, 'quantity': 1, 'is_send_to_gift': False}]
                # 'user_items': {'item_cards': [{'id': 9117946, 'card_id': 1002640, 'quantity': 2}]
                print(colors.render('{success}claimed ' + str(len(missions)) + ' missions.'))
            else:
                error.handler('mission accept', store2)
        else:
            print(colors.render('{error}no missions to claim!'))
    else:
        error.handler('mission', store)


# summon
def summon(banner_id, course):
    settings = funcs.get_settings()
    # 'gasha_items': [{'item_id': 1000770, 'item_type': 'Card', 'card_exp_init': 0, 'quantity': 1}]
    # 'user_items': {'cards': [{'id': 1291989142, 'card_id': 1000770, 'exp': 0, 'skill_lv': 1, 'is_favorite': False, 'awakening_route_id': None, 'is_released_potential': False, 'released_rate': 0.0, 'optimal_awakening_step': None, 'card_decoration_id': None, 'awakenings': [], 'unlocked_square_statuses': [], 'updated_at': 1607350936, 'created_at': 1607350936, 'potential_parameters': [], 'equipment_skill_items': [], 'link_skill_lvs': []}]
    store = ingame.summon(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, banner_id, course)
    if 'error' not in store:
        if 'cards' in store['user_items']:
            card_ids = store['user_items']['cards']
        else:
            card_ids = None
        if 'item_cards' in store['user_items']:
            item_cards = store['user_items']['item_cards']
        else:
            item_cards = None
        caches.add_cards(card_ids, item_cards)
        if settings['animations']:
            print(store['movie'])
        cards = []
        card_ids = []
        if not settings['display_only_ids']:
            for i in store['gasha_items']:
                try:
                    card_text = funcs.render_card_text(i, True, True, False)
                    cards.append(card_text)
                except:
                    if settings['display_ids']:
                        cardId = ' (' + str(i['item_id']) + ')'
                    else:
                        cardId = ''
                    cards.append('unknown (' + str(i['item_id']) + ') x' + str(i['quantity']) + cardId)
                card_ids.append(str(i['item_id']))
        else:
            for i in store['gasha_items']:
                cards.append(str(i['item_id']) + ' x' + str(i['quantity']))
        print(',\n'.join(cards))
        if settings['summon_sell']:
            if settings['autosell']:
                sell_useless()
                if settings['baba_useless']:
                    baba_useless()
        if settings['potential_node']:
            print(colors.render('{message}checking for dupes...'))
            for i in caches.cards:
                card = json.loads(i[3])
                # check only for UR units
                if str(int(i[1]) - 1) in card_ids:
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
            # TODO reverse if card is TUR/LR then reawaken if in settings
    else:
        error.handler('summon', store)


# stam restore
def restore():
    settings = funcs.get_settings()
    if settings['stam_use_stone'] and not settings['stam_use_item']:
        store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
        if int(store['user']['stone']) >= 1:
            print(colors.render('{message}refilling stamina...'))
            store = ingame.act_refill(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            if 'error' not in store:
                print(colors.render('{success}stamina restored.'))
                return True
            else:
                error.handler('restore', store)
                return False
        else:
            print(colors.render('{error}not enough stones.'))
            return False
    elif settings['stam_use_item']:
        store = ingame.login_resources(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            for i in store['act_items']:
                if i['quantity'] >= 1:
                    store = ingame.item_act_refill(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                                   i['act_item_id'], 1)
                    if 'error' not in store:
                        print(colors.render('{success}stamina restored by item.'))
                        break
                    else:
                        error.handler('act-item', store)
                        continue
        else:
            error.handler('sitems', store)
    else:
        print(colors.render('{error}Use stones is set to "OFF"'))
        return False


# organize drops to display correctly
def organize_rewards(which, drops):
    settings = funcs.get_settings()
    rewards = []
    already_stacked = []
    stacked_items = []
    card_objs = []
    item_cards = []
    # 'user_items': {'cards': [{'id': 1071236919, 'card_id': 1005610, 'exp': 497813, 'skill_lv': 1, 'is_favorite': False, 'awakening_route_id': None, 'is_released_potential': False, 'released_rate': 0.0, 'optimal_awakening_step': None, 'card_decoration_id': None, 'awakenings': [], 'unlocked_square_statuses': [], 'updated_at': 1607351705, 'created_at': 1575753656, 'potential_parameters': [], 'equipment_skill_items': [], 'link_skill_lvs': [{'id': 22, 'skill_lv': 4}, {'id': 23, 'skill_lv': 3}, {'id': 30, 'skill_lv': 4}, {'id': 34, 'skill_lv': 4}, {'id': 39, 'skill_lv': 5}, {'id': 47, 'skill_lv': 4}, {'id': 66, 'skill_lv': 5}]}]}
    # print('drops boost activated: ' + str(drops['boosted']))
    if settings['display_drops']:
        if which == 'stage':
            if 'items' in drops:
                if 'user_items' in drops:
                    if 'cards' in drops['user_items']:
                        for i in drops['user_items']['cards']:
                            if database.query(f"./boxes/{caches.loaded}.db", 'cards', 'id=' + str(i['id']), 0) is None:
                                card_objs.append(i)
                    if 'item_cards' in drops['user_items']:
                        for i in drops['user_items']['item_cards']:
                            item_cards.append(i)
                    caches.add_cards(card_objs, item_cards)
                if settings['stack_drops']:
                    for i in drops['items']:
                        if i['item_id'] not in already_stacked:
                            already_stacked.append(i['item_id'])
                            stacked_items.append({'item_id': i['item_id'], 'item_type': i['item_type'], 'quantity': i['quantity']})
                        else:
                            for x in stacked_items:
                                if x['item_id'] == i['item_id'] and x['item_type'] == i['item_type']:
                                    stacked_items.remove(x)
                                    x['quantity'] = int(x['quantity']) + int(i['quantity'])
                                    stacked_items.append(x)
                                    break
                            continue
                    items = stacked_items
                else:
                    items = drops['items']
                if settings['display_drop_names']:
                    if 'zeni' in drops:
                        rewards.append('Zeni: ' + str(drops['zeni']))
                    if 'gasha_point' in drops:
                        rewards.append('FP: ' + str(drops['gasha_point']))
                    if 'quest_clear_rewards' in drops:
                        for x in drops['quest_clear_rewards']:
                            if x['item_type'] == 'Point::Stone':
                                rewards.append('Stone x' + str(x['amount']))
                    if 'dragonballs' in drops:
                        for x in drops['dragonballs']:
                            rewards.append('Dragonball #' + str(x['num']))
                    for x in items:
                        if x['item_type'] == 'SupportItem':
                            try:
                                rewards.append(
                                    database.fetch(caches.acc_ver + '.db', 'support_items',
                                                   'id=' + str(x['item_id']))[
                                        1] + ' x' + str(
                                        x['quantity']))
                            except:
                                rewards.append('support x' + str(x['quantity']))
                        if x['item_type'] == 'PotentialItem':
                            try:
                                rewards.append(
                                    database.fetch(caches.acc_ver + '.db', 'potential_items',
                                                   'id=' + str(x['item_id']))[
                                        1] + ' x' + str(
                                        x['quantity']))
                            except:
                                rewards.append('orb x' + str(x['quantity']))
                        if x['item_type'] == 'TrainingItem':
                            try:
                                rewards.append(
                                    database.fetch(caches.acc_ver + '.db', 'training_items',
                                                   'id=' + str(x['item_id']))[
                                        1] + ' x' + str(
                                        x['quantity']))
                            except:
                                rewards.append('training item x' + str(x['quantity']))
                        if x['item_type'] == 'AwakeningItem':
                            try:
                                rewards.append(
                                    database.fetch(caches.acc_ver + '.db', 'awakening_items',
                                                   'id=' + str(x['item_id']))[
                                        1] + ' x' + str(
                                        x['quantity']))
                            except:
                                rewards.append('medal x' + str(x['quantity']))
                        if x['item_type'] == 'TreasureItem':
                            try:
                                rewards.append(
                                    database.fetch(caches.acc_ver + '.db', 'treasure_items',
                                                   'id=' + str(x['item_id']))[
                                        1] + ' x' + str(
                                        x['quantity']))
                            except:
                                rewards.append('treasure x' + str(x['quantity']))
                        if x['item_type'] == 'Card':
                            card_text = funcs.render_card_text(x, True, True, False)
                            rewards.append(card_text + '{drops}')
                else:
                    if 'zeni' in drops:
                        rewards.append('Zeni: ' + str(drops['zeni']))
                    if 'gasha_point' in drops:
                        rewards.append('FP: ' + str(drops['gasha_point']))
                    if 'quest_clear_rewards' in drops:
                        for x in drops['quest_clear_rewards']:
                            if x['item_type'] == 'Point::Stone':
                                rewards.append('Stone x' + str(x['amount']))
                    if 'items' in drops:
                        for x in drops['items']:
                            if x['item_type'] == 'SupportItem':
                                rewards.append('support x' + str(x['quantity']))
                            if x['item_type'] == 'PotentialItem':
                                rewards.append('orb x' + str(x['quantity']))
                            if x['item_type'] == 'TrainingItem':
                                rewards.append('training item x' + str(x['quantity']))
                            if x['item_type'] == 'AwakeningItem':
                                rewards.append('medal x' + str(x['quantity']))
                            if x['item_type'] == 'TreasureItem':
                                rewards.append('treasure x' + str(x['quantity']))
                            if x['item_type'] == 'Card':
                                rewards.append('card x' + str(x['quantity']))
                    if 'dragonballs' in drops:
                        for x in drops['dragonballs']:
                            rewards.append('Dragonball #' + str(x['num']))
        if which == 'eza':
            if settings['display_drop_names']:
                if 'user' in drops:
                    if 'zeni' in drops['user']:
                        rewards.append('Zeni: ' + str(drops['user']['zeni']))
                    if 'gasha_point' in drops['user']:
                        rewards.append('FP: ' + str(drops['user']['gasha_point']))
                    if 'exchange_point' in drops['user']:
                        rewards.append('BP: ' + str(drops['user']['exchange_point']))
                    if 'stone' in drops['user']:
                        rewards.append('Stones: ' + str(1))
                if 'cards' in drops:
                    for x in drops['cards']:
                        try:
                            card_text = funcs.render_card_text(x, True, False, False)
                            rewards.append(card_text + 'x1')
                        except:
                            rewards.append('card x1')
                if 'awakening_items' in drops:
                    for x in drops['awakening_items']:
                        try:
                            rewards.append(database.fetch(caches.acc_ver + '.db', 'awakening_items',
                                                          'id=' + str(x['awakening_item_id']))[
                                               1] + ' x' + str(x['quantity']))
                        except:
                            rewards.append('medal x' + str(x['quantity']))
                if 'potential_items' in drops:
                    for x in drops['potential_items']:
                        try:
                            rewards.append(database.fetch(caches.acc_ver + '.db', 'potential_items',
                                                          'id=' + str(x['potential_item_id']))[
                                               1] + ' x' + str(x['quantity']))
                        except:
                            rewards.append('orb x' + str(x['quantity']))
            else:
                if 'user' in drops:
                    if 'zeni' in drops['user']:
                        rewards.append('Zeni: ' + str(drops['user']['zeni']))
                    if 'gasha_point' in drops['user']:
                        rewards.append('FP: ' + str(drops['user']['gasha_point']))
                    if 'exchange_point' in drops['user']:
                        rewards.append('BP: ' + str(drops['user']['exchange_point']))
                    if 'stone' in drops['user']:
                        rewards.append('Stones: ' + str(1))
                if 'cards' in drops:
                    for x in drops['cards']:
                        rewards.append('card x1')
                if 'awakening_items' in drops:
                    for x in drops['awakening_items']:
                        rewards.append('medal x' + str(x['quantity']))
                if 'potential_items' in drops:
                    for x in drops['potential_items']:
                        rewards.append('orb x' + str(x['quantity']))
        if which == 'clash':
            if settings['display_drop_names']:
                if 'items' in drops:
                    for x in drops['items']:
                        if x['item_type'] == 'Point::Stone':
                            rewards.append('Stone x' + str(x['quantity']))
                        if x['item_type'] == 'TreasureItem':
                            try:
                                rewards.append(
                                    database.fetch(caches.acc_ver + '.db', 'treasure_items', 'id=' + str(x['item_id']))[
                                        1] + ' x' + str(x['quantity']))
                            except:
                                rewards.append('treasure x' + str(x['quantity']))
            else:
                if 'items' in drops:
                    for x in drops['items']:
                        if x['item_type'] == 'Point::Stone':
                            rewards.append('Stone x' + str(x['quantity']))
                        if x['item_type'] == 'TreasureItem':
                            rewards.append('treasure x' + str(x['quantity']))
        print(colors.render('{drops}' + ',\n'.join(rewards)))


# pick support & build team according to conditions
def handle_condition(limits, cards, stage):
    build_team = True
    '''if str(str(stage)[0:3]) != '712':
        build_team = True
    else:
        if '"is_friend": true' in json.dumps(cards):
            build_team = True
        else:
            build_team = False'''
    if build_team:
        friend = cards[0]['id']
        friend_card = cards[0]['leader']['card_id']
        if limits is not None:
            settings = funcs.get_settings()
            if settings['team_builder']:
                built = autoteam.build(limits, cards, stage)
                if built[0] is not None and built[1] is not None:
                    friend = built[0]
                    friend_card = built[1]
        return [friend, friend_card]
    else:
        return [False, False]


# generate simulated map movement
def simulate_map(sugoroku, which, enemies=None):
    if which == 'stage':
        # 5010:0
        paces = []
        defeated = []
        for i in sugoroku['events'].keys():
            paces.append(int(i))
        for i in sugoroku['events']:
            if 'battle_info' in sugoroku['events'][i]['content']:
                for j in sugoroku['events'][i]['content']['battle_info']:
                    defeated.append(j['round_id'])
        return [paces, defeated]
    if which == 'round':
        dice = random.randint(0, 6)


# run stage
def run_stage(stage, difficulty, kagi, return_drops=None, deck=None, boostable=False):
    # stage information
    events = caches.events
    # support
    store = ingame.get_supports(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, stage, difficulty)
    if 'error' not in store:
        difficulties = ['normal', 'hard', 'very_hard', 'super_hard1', 'super_hard2', 'super_hard3']
        friend = None
        friend_card = None
        if len(str(stage)) == 4 or len(str(stage)) == 5:
            supports = handle_condition(None, store['supporters'], stage)
            friend = supports[0]
            friend_card = supports[1]
        else:
            limits = None
            if int(database.fetch(caches.acc_ver + '.db', 'sugoroku_maps', 'quest_id=' + str(stage))[17]) == 1:
                friends = store['cpu_supporters'][str(difficulties[int(difficulty)])]['cpu_friends']
            else:
                if 'cpu_supporters' in store:
                    if str(difficulties[int(difficulty)]) in store['cpu_supporters']:
                        friends = store['cpu_supporters'][str(difficulties[int(difficulty)])]['cpu_friends']
                        if len(friends) == 0:
                            friends = store['supporters']
                    else:
                        friends = store['supporters']
                else:
                    friends = store['supporters']
            for event in events['events']:
                if str(event['id']) == str(stage)[0:3]:
                    for i in event['quests']:
                        if 'limitations' in i and len(i['limitations']) != 0:
                            limits = i['limitations']
            supports = handle_condition(limits, friends, stage)
            friend = supports[0]
            friend_card = supports[1]
        # start
        if stage is not None and difficulty is not None and friend is not None and friend_card is not None and friend:
            timer_start = int(round(time.time(), 0))
            store = ingame.start_stage(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, stage, difficulty, friend, friend_card, kagi, deck, boostable)
            if 'error' not in store:
                data = crypto.decrypt_sign(caches.acc_ver, store['sign'])
                #print(data)
                stoken = data['token']
                map_data = simulate_map(data['sugoroku'], 'stage', None)
                paces, defeated = map_data[0], map_data[1]
                # finish
                store = ingame.finish_stage(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, stage, difficulty, paces, defeated, stoken)
                if 'error' not in store:
                    # rewards
                    timer_finish = int(round(time.time(), 0))
                    timer_total = timer_finish - timer_start
                    print(colors.render('{success}cleared stage in ' + str(timer_total) + ' seconds.'))
                    data = crypto.decrypt_sign(caches.acc_ver, store['sign'])
                    organize_rewards('stage', data)
                    if return_drops:
                        return data
                else:
                    error.handler('finish', store)
            else:
                error.handler('start', store, stage, difficulty, kagi, return_drops, boostable)
                if return_drops:
                    return False
        else:
            if not friend:
                '''for i in friends:
                    print(str(i['name']) + ' - ' + str(i['is_friend']))'''
                print(colors.render('{error}No friend found for LGE 200 FP.'))
                #runStage(stage, difficulty, kagi, return_drops)
            else:
                print(colors.render('{error}No support/not enough units/event not up.'))
    else:
        error.handler('support', store)
        '''if 'invalid_token' in store['error']:
            funcs.refresh()'''


# run eza level
def run_z_lvl(eza, level):
    # level information
    settings = funcs.get_settings()
    area = None
    if settings['display_stage_names']:
        if len(str(eza)) >= 1:
            try:
                area = database.fetch(caches.acc_ver + '.db', 'z_battle_stage_views', 'z_battle_stage_id=' + str(eza))[3]
            except:
                area = 'unknown #' + str(eza)
    else:
        area = str(eza)
    print(colors.render('{message}' + str(area) + ' EZA - Level ' + str(level)))
    em_hp = []
    em_atk = 0
    # support
    store = ingame.z_supports(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, eza)
    if 'error' not in store:
        friend = store['supporters'][0]['id']
        friend_card = store['supporters'][0]['leader']['card_id']
        timer_start = int(round(time.time(), 0))
        # start
        if eza is not None and level is not None and friend is not None and friend_card is not None:
            store = ingame.z_start(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, eza, level,
                                  friend, friend_card)
            if 'error' not in store:
                dec_sign = crypto.decrypt_sign(caches.acc_ver, store['sign'])
                for i in dec_sign['enemies'][0]:
                    em_hp.append(i['hp'])
                    em_atk = int(em_atk) + int(i['attack'])
                stoken = dec_sign['token']
                # end
                store = ingame.z_finish(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, eza, level,
                                       stoken, em_atk, em_hp)
                if 'error' not in store:
                    # rewards
                    timer_finish = int(round(time.time(), 0))
                    timer_total = timer_finish - timer_start
                    print(colors.render(
                        '{success}completed level: ' + str(level) + ' in ' + str(timer_total) + ' seconds.'))
                    dec_sign = crypto.decrypt_sign(caches.acc_ver, store['sign'])
                    organize_rewards('eza', dec_sign['user_items'])
                else:
                    error.handler('zfinish', store)
            else:
                error.handler('zstart', store)
        else:
            print(colors.render('{error}No friend/not enough units / event not up.'))
    else:
        error.handler('zsupport', store)
        if 'invalid_token' in store['error']:
            # funcs.refresh()
            run_z_lvl(eza, level)


# run clash level
def run_clash_lvl(clash, level, cards, begin):
    # level information
    print(colors.render('{message}' + 'starting Clash #' + str(clash) + ' - lvl. ' + str(level) + '...'))
    leader = cards[0]
    cards.remove(cards[0])
    sub = cards[1]
    cards.remove(cards[1])
    team = []
    for i in cards:
        if len(team) < 5 and i not in team:
            team.append(i)
        else:
            break
    # start
    store = ingame.clash_start(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, clash, level, begin, leader, sub, team)
    if 'error' not in store:
        data = crypto.decrypt_sign(caches.acc_ver, store['sign'])
        hp = data['continuous_info']['remaining_hp']
        round = data['continuous_info']['round']
        stoken = data['token']
        # end
        store = ingame.clash_end(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, clash, hp, round, stoken)
        if 'error' not in store:
            # rewards
            print(colors.render('{success}completed: lvl. ' + str(level)))
            if 'sign' in store:
                data = crypto.decrypt_sign(caches.acc_ver, store['sign'])
                organize_rewards('clash', data)
            else:
                organize_rewards('clash', store)
            return True
        else:
            error.handler('bfEnd', store)
            return False
    else:
        error.handler('bfStart', store)
        return False
        #print(str(clash) + ' - ' + str(level))
        # "{'error': {'code': 'stage_not_found_in_current_rmbattle_level'}}"


# handle stage information before run
def handler(which, stage, difficulty, kagi=None, return_drops=None, boost=False):
    #print('handler')
    settings = funcs.get_settings()
    area_id, area, name, match = None, None, None, None
    # quest/event
    if which == 0:
        sugoroku = database.fetchAll(caches.acc_ver + '.db', 'sugoroku_maps', 'id=' + str(stage) + str(difficulty))
        quest = database.fetch(caches.acc_ver + '.db', 'quests', 'id=' + str(stage))
        if sugoroku is not None and len(sugoroku) != 0 and quest is not None and len(quest) != 0:
            if len(str(stage)) == 4:
                area_id = str(stage)[0:1]
            elif len(str(stage)) == 5:
                area_id = str(stage)[0:2]
            elif len(str(stage)) == 6:
                area_id = str(stage)[0:3]
            if settings['display_stage_names']:
                try:
                    area = database.fetch(caches.acc_ver + '.db', 'areas', 'id=' + str(area_id))[4]
                    name = quest[2]
                    match = str(area) + ' - ' + str(name) + ' (' + str(stage) + ':' + str(difficulty) + ')'
                except:
                    area, name = 'unknown', 'unknown'
                    match = str(name) + ' (' + str(stage) + ':' + str(difficulty) + ')'
            else:
                match = str(stage) + ':' + str(difficulty)
            # check if area is allowed to be cleared
            areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            if 'error' not in areas:
                active_area_ids = []
                for i in areas['user_areas']:
                    active_area_ids.append(int(i['area_id']))
                if int(area_id) in active_area_ids:
                    # get boost if toggled
                    if settings['drops_boost']:
                        store99 = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret,
                                              False)
                        if 'error' not in store99:
                            user = store99['user']
                            if int(user['boost_point']) >= 1 and quest[12] is not None and int(quest[12]) > 0:
                                boost = True
                                print(colors.render(
                                    '{message}[!] Using bonus #' + str(user['boost_point']) + '!'))
                            else:
                                boost = False
                        else:
                            error.handler('boostChck', store99)
                            boost = False
                    # if event; check if event is available
                    if len(str(stage)) >= 6:
                        events = caches.events
                        active_event_ids = []
                        for event in events['events']:
                            active_event_ids.append(event['id'])
                        if int(area_id) in active_event_ids:
                            decks = caches.teams
                            print(colors.render('{message}' + match))
                            drops = run_stage(stage, difficulty, kagi, return_drops, decks['selected_team_num'], boost)
                            if return_drops:
                                return drops
                        elif settings['use_keys']:
                            area_query = database.fetch(caches.acc_ver + '.db', 'areas', 'id=' + str(area_id))
                            if area_query is not None:
                                area_category = area_query[2]
                                keys = database.fetchAll(caches.acc_ver + '.db', 'eventkagi_items', None)
                                for k in keys:
                                    if int(area_category) in json.loads(k[4])['area_category_ids']:
                                        print(
                                            colors.render(
                                                '{message}[!] Using key (' + str(k[0]) + ') to clear event.'))
                                        decks = caches.teams
                                        print(colors.render('{message}' + match))
                                        drops = run_stage(stage, difficulty, k[0], return_drops,
                                                          decks['selected_team_num'])
                                        if return_drops:
                                            return drops
                    else:
                        decks = caches.teams
                        print(colors.render('{message}' + match))
                        drops = run_stage(stage, difficulty, kagi, return_drops, decks['selected_team_num'], boost)
                        if return_drops:
                            return drops
            else:
                error.handler('handleAreas', areas)
        else:
            print(colors.render('{error}Stage (' + str(stage) + ') is not in database.'))
    # EZA
    if which == 1:
        pass
    # clash
    if which == 2:
        pass


# streamline - from last to finish
def streamline(which):
    if which == 'quests':
        decks = caches.teams
        settings = funcs.get_settings()
        user = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
        if 'error' not in user:
            if int(user['user']['stone']) >= 1:
                areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                if 'error' not in areas:
                    # user_areas -> area_id -> user_sugoroku_maps -> sugoroku_map_id, cleared_count
                    maps = []
                    for i in areas['user_areas']:
                        if i['area_id'] <= 27:
                            for j in i['user_sugoroku_maps']:
                                if j['cleared_count'] == 0:
                                    maps.append(j['sugoroku_map_id'])
                    if len(maps) == 0:
                        print(colors.render('{error}no quests to complete.'))
                    else:
                        f = open('./farming/quests.txt', 'r')
                        content = f.read()
                        f.close()
                        quests = content.split('\n')
                        print(colors.render('{message}getting last stage cleared...'))
                        for i in quests:
                            if int(i) >= int(maps[0]):
                                #handler(0, str(str(i)[:-1]), str(i)[-1])
                                quest = database.fetch(caches.acc_ver + '.db', 'quests', 'id=' + str(i)[:-1])
                                if len(str(i)[:-1]) == 4:
                                    area_id = str(str(i)[:-1])[0:1]
                                elif len(str(i)[:-1]) == 5:
                                    area_id = str(str(i)[:-1])[0:2]
                                elif len(str(i)[:-1]) == 6:
                                    area_id = str(str(i)[:-1])[0:3]
                                if settings['display_stage_names']:
                                    try:
                                        area = database.fetch(caches.acc_ver + '.db', 'areas', 'id=' + str(area_id))[4]
                                        name = quest[2]
                                        match = str(area) + ' - ' + str(name) + ' (' + str(i)[:-1] + ':' + str(i)[-1] + ')'
                                    except:
                                        area, name = 'unknown', 'unknown'
                                        match = str(name) + ' (' + str(i)[:-1] + ':' + str(i)[-1] + ')'
                                else:
                                    match = str(i)[:-1] + ':' + str(i)[-1]
                                print(colors.render('{message}' + match))
                                run_stage(str(i)[:-1], str(i)[-1], None, None, decks['selected_team_num'], False)
                else:
                    error.handler('strmlineAreas', areas)
            else:
                print(colors.render('{error}not enough stones.'))
        else:
            error.handler('qUser', user)
    if which == 'events':
        decks = caches.teams
        settings = funcs.get_settings()
        user = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
        if 'error' not in user:
            if int(user['user']['stone']) >= 1:
                events = caches.events
                event_ids = []
                for event in events['events']:
                    event_ids.append(event['id'])
                    event_ids = sorted(event_ids)
                # Complete areas if they are in the current ID pool
                areas = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
                i = 1
                for area in areas['user_areas']:
                    if area['area_id'] in event_ids:
                        for stage in area['user_sugoroku_maps']:
                            if stage['cleared_count'] == 0:
                                #handler(0, str(str(stage['sugoroku_map_id'])[:-1]), str(stage['sugoroku_map_id'])[-1])
                                quest = database.fetch(caches.acc_ver + '.db', 'quests', 'id=' + str(stage['sugoroku_map_id'])[:-1])
                                if settings['display_stage_names']:
                                    area_db = database.fetch(caches.acc_ver + '.db', 'areas', 'id=' + str(area['area_id']))[4]
                                    name = quest[2]
                                    match = str(area_db) + ' - ' + str(name) + ' (' + str(stage['sugoroku_map_id'])[
                                                                                   :-1] + ':' + \
                                            str(stage['sugoroku_map_id'])[-1] + ')'
                                else:
                                    match = str(stage['sugoroku_map_id'])[:-1] + ':' + str(stage['sugoroku_map_id'])[-1]
                                print(colors.render('{message}' + match))
                                run_stage(str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1], None, None, decks['selected_team_num'], False)
                                continue
                    if i % 30 == 0:
                        funcs.refresh()
            else:
                print(colors.render('{error}not enough stones.'))
        else:
            error.handler('eUser', user)
    if which == 'ezas':
        store = caches.events
        eza_pool = []
        if 'z_battle_stages' in store:
            for x in store['z_battle_stages']:
                eza_pool.append(int(x['id']))
            store = ingame.quests(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
            for i in eza_pool:
                for x in store['user_z_battles']:
                    if int(x['z_battle_stage_id']) == int(i):
                        clear_count = int(x['max_clear_level'])
                        if clear_count == 0:
                            clear_count = clear_count + 1
                        if clear_count < 30:
                            while int(clear_count) <= 30:
                                if clear_count != 0:
                                    run_z_lvl(int(i), int(clear_count))
                                    clear_count = clear_count + 1
                        else:
                            print(colors.render('{error}This EZA has already been cleared.'))
        else:
            caches.update_events()
            streamline('ezas')
    if which == 'clash':
        team = None
        begin = True
        # current clash
        store = ingame.home_resources(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret)
        if 'error' not in store:
            if 'id' in store['rmbattles']:
                #print(store['rmbattles'])
                clash = store['rmbattles']['id']
                # current lvl
                store = ingame.clash_info(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, clash)
                if 'error' not in store:
                    # get clash cards
                    if 'current_level_info' in store:
                        current_lvl = int(store['current_level_info']['level'])
                        if 'sortiable_user_card_ids' in store['current_level_info']:
                            cards = store['current_level_info']['sortiable_user_card_ids']
                        else:
                            print(colors.render('{error}No cards to run clash!'))
                            return
                    else:
                        current_lvl = 1
                        cards = ingame.clash_cards(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, 1)
                    # sort clash cards
                    already_used = []
                    if 'used_decks' in store:
                        for i in store['level_stages'].keys():
                            if i in store['used_decks']:
                                if store['used_decks'][i]['used_card_ids'][0]['leader'] in cards:
                                    cards.remove(store['used_decks'][i]['used_card_ids'][0]['leader'])
                                if store['used_decks'][i]['used_card_ids'][0]['sub_leader'] in cards:
                                    cards.remove(store['used_decks'][i]['used_card_ids'][0]['sub_leader'])
                                for x in store['used_decks'][i]['used_card_ids'][0]['members']:
                                    if x in cards:
                                        cards.remove(i)
                    # determine if first run
                    if 'sortiable_user_card_ids' in cards:
                        team = cards['sortiable_user_card_ids']
                        begin = False
                    elif 'user_card_ids' in cards:
                        if len(cards['user_card_ids']) != 0:
                            team = cards['user_card_ids']
                            begin = True
                        else:
                            print(colors.render('{error}No cards to run clash!'))
                            return
                    elif 'current_level_info' in cards:
                        team = cards['current_level_info']['sortiable_user_card_ids']
                        begin = False
                    elif type(cards) == list:
                        team = cards
                        begin = False
                    # loop levels
                    if team is not None:
                        for i in store['level_stages'].keys():
                            # if begin == False and currentLvl == int(i):
                            #   i = currentLvl
                            for x in store['level_stages'][i]:
                                if int(x['remaining_hp']) != 0:
                                    if 'sortiable_user_card_ids' in x:
                                        team = x['sortiable_user_card_ids']
                                        begin = False
                                    level_ran = run_clash_lvl(clash, x['id'], team, begin)
                                    if level_ran:
                                        store = ingame.clash_info(caches.acc_ver, caches.acc_os, caches.sess_token,
                                                                  caches.sess_secret, clash)
                                        if 'current_level_info' in store:
                                            if 'sortiable_user_card_ids' in store['current_level_info']:
                                                cards = store['current_level_info']['sortiable_user_card_ids']
                                                team = cards
                                                begin = False
                                            else:
                                                print(colors.render('{error}No cards to run clash!'))
                                                break
                                    else:
                                        break
                    else:
                        print(colors.render('{error}no cards to clear clash!'))
                else:
                    error.handler('clashInfo', store)
            else:
                print(colors.render('{error}clash isn\'t active!'))
        else:
            error.handler('resources1', store)
    # area streamline
    if isinstance(which, int) and len(str(which)) == 3:
        pass
