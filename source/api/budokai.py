import requests
import json
import time
from random import randint
import config as config
import utils.crypto as crypto

# request list of rounds & overall information
def entryInfo(ver, os, token, secret, budokai):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/budokais/' + str(budokai) + '/entry'
        auth = crypto.mac(ver, token, secret, 'GET', '/budokais/' + str(budokai) + '/entry')
        code = config.gb_code[str(os)]
        asset = config.file_ts1
        db = config.db_ts1
    else:
        url = config.jp_url + '/budokais/' + str(budokai) + '/entry'
        auth = crypto.mac(ver, token, secret, 'GET', '/budokais/' + str(budokai) + '/entry')
        code = config.jp_code[str(os)]
        asset = config.file_ts2
        db = config.db_ts2
    headers = {
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'X-Language': config.lang,
        'User-Agent': dua
        }
    r = requests.get(url, data=None, headers=headers)
    return r.json()

# request WT supports
def supports(ver, os, token, secret):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/quests/0/supporters'
        auth = crypto.mac(ver, token, secret, 'GET', '/quests/0/supporters')
        code = config.gb_code[str(os)]
        asset = config.file_ts1
        db = config.db_ts1
    else:
        url = config.jp_url + '/quests/0/supporters'
        auth = crypto.mac(ver, token, secret, 'GET', '/quests/0/supporters')
        code = config.jp_code[str(os)]
        asset = config.file_ts2
        db = config.db_ts2
    headers = {
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'X-Language': config.lang,
        'User-Agent': dua
        }
    r = requests.get(url, data=None, headers=headers)
    return r.json()

# request round stage ID
def tournament(ver, os, token, secret, budokai, friend, motivation, deck):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/budokais/' + str(budokai) + '/tournaments'
        auth = crypto.mac(ver, token, secret, 'POST', '/budokais/' + str(budokai) + '/tournaments')
        code = config.gb_code[str(os)]
        asset = config.file_ts1
        db = config.db_ts1
    else:
        url = config.jp_url + '/budokais/' + str(budokai) + '/tournaments'
        auth = crypto.mac(ver, token, secret, 'POST', '/budokais/' + str(budokai) + '/tournaments')
        code = config.jp_code[str(os)]
        asset = config.file_ts2
        db = config.db_ts2
    headers = {
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'X-Language': config.lang,
        'User-Agent': dua
        }
    data = {
        'friend_id': int(friend),
        'motivation_id': int(motivation),
        'selected_team_num': int(deck),
        'support_items': []
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

# start WT round
def startRound(ver, os, token, secret, budokai, roundId, friend, deck):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/start'
        auth = crypto.mac(ver, token, secret, 'POST', '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/start')
        code = config.gb_code[str(os)]
        asset = config.file_ts1
        db = config.db_ts1
    else:
        url = config.jp_url + '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/start'
        auth = crypto.mac(ver, token, secret, 'POST', '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/start')
        code = config.jp_code[str(os)]
        asset = config.file_ts2
        db = config.db_ts2
    headers = {
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'X-Language': config.lang,
        'User-Agent': dua
        }
    data = {
        'friend_id': int(friend),
        'selected_team_num': int(deck),
        'support_items': []
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

# end WT round
def finishRound(ver, os, token, secret, budokai, roundId, steps, actions, hp, stoken):
    if os == 'android':
        dua = config.device_agent1
    else:
        dua = config.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/finish'
        auth = crypto.mac(ver, token, secret, 'POST', '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/finish')
        code = config.gb_code[str(os)]
        asset = config.file_ts1
        db = config.db_ts1
    else:
        url = config.jp_url + '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/finish'
        auth = crypto.mac(ver, token, secret, 'POST', '/budokais/' + str(budokai) + '/tournaments/' + str(roundId) + '/finish')
        code = config.jp_code[str(os)]
        asset = config.file_ts2
        db = config.db_ts2
    headers = {
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'X-Language': config.lang,
        'User-Agent': dua
        }
    finish = int(round(time.time(), 0) + 90)
    start = finish - randint(6200000, 8200000)
    data = {
        'actual_steps': steps,
        'budokai': {
            'actions': actions,
            'hp': int(hp)
        },
        'difficulty': 0,
        'elapsed_time': finish - start,
        'is_cheat_user': False,
        'is_cleared': False,
        'quest_id': 0,
        'scripts': [],
        'steps': steps,
        'token': stoken,
        'used_items': []
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()