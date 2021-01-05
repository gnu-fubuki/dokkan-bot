import requests
import json
import config as config
import api.caches as caches
import utils.crypto as crypto

def validate(ver, tc, fc):
    if ver == 'gb':
        url = config.gb_url + '/auth/link_codes/' + str(tc) + '/validate'
        code = config.gb_code['android']
    else:
        url = config.jp_url + '/auth/link_codes/' + str(tc) + '/validate'
        code = config.jp_code['android']
    headers = {
        'Accept': '*/*',
        'X-Language': caches.lang,
        'X-Platform': 'android',
        'X-ClientVersion': code,
        'Content-Type': 'application/json',
        'User-Agent': caches.device_agent1
    }
    data = {'eternal': True,'user_account': {'platform': 'android','user_id': fc}}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

def use(ver, os, tc, fc):
    if os == 'android':
        dn = caches.device_name1
        dm = caches.device_model1
        dv = caches.device_ver1
        dua = caches.device_agent1
    else:
        dn = caches.device_name2
        dm = caches.device_model2
        dv = caches.device_ver2
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/auth/link_codes/' + str(tc)
        code = config.gb_code[str(os)]
    else:
        url = config.jp_url + '/auth/link_codes/' + str(tc)
        code = config.jp_code[str(os)]
    headers = {
        'Accept': '*/*',
        'X-Language': caches.lang,
        'X-Platform': os,
        'X-ClientVersion': code,
        'Content-Type': 'application/json',
        'User-Agent': dua
    }
    data = {'eternal': True,'old_user_id': '','user_account': {'device': dn,'device_model': dm,'os_version': dv,'platform': os,'unique_id': caches.uuid}}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    return r.json()

def create(ver, os, token, secret):
    if os == 'android':
        dua = caches.device_agent1
    else:
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/auth/link_codes'
        auth = crypto.mac(ver, token, secret, 'POST', '/auth/link_codes')
        code = config.gb_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts
    else:
        url = config.jp_url + '/auth/link_codes'
        auth = crypto.mac(ver, token, secret, 'POST', '/auth/link_codes')
        code = config.jp_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts
    headers = {
        'X-Platform': os,
        'X-Language': caches.lang,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': auth,
        'User-Agent': dua
    }
    data = {'eternal':True}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

# validate whether account is linked
def facebookValidate(ver, os, id, token):
    if os == 'android':
        dua = caches.device_agent1
    else:
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/user/succeed/facebook/validate'
        code = config.gb_code[str(os)]
    else:
        url = config.jp_url + '/user/succeed/facebook/validate'
        code = config.jp_code[str(os)]

    sign = {'facebook_id': str(id),'facebook_token': str(token)}

    enc_sign = crypto.encrypt_sign(json.dumps(sign))

    headers = {
        'Accept': '*/*',
        'X-Language': caches.lang,
        'X-Platform': os,
        'X-ClientVersion': code,
        'Content-Type': 'application/json',
        'User-Agent': dua
    }
    data = {'sign': enc_sign}

    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

# get identifier from sign encrypted facebook ID & OAuth token
def facebook(ver, os, id, token):
    if os == 'android':
        dn = caches.device_name1
        dm = caches.device_model1
        dv = caches.device_ver1
        dua = caches.device_agent1
    else:
        dn = caches.device_name2
        dm = caches.device_model2
        dv = caches.device_ver2
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/user/succeed/facebook'
        code = config.gb_code[str(os)]
        sign = {'facebook_id': str(id),'facebook_token': str(token),'user_account': {'device': dn,'device_model': dm,'os_version': dv,'platform': os,'unique_id': caches.uuid}}
    else:
        url = config.jp_url + '/user/succeed/facebook'
        code = config.jp_code[str(os)]
        sign = {'facebook_id': str(id),'facebook_token': str(token),'user_account': {'device': dn,'device_model': dm,'os_version': dv,'platform': os,'unique_id': caches.uuid}}

    enc_sign = crypto.encrypt_sign(ver, json.dumps(sign))

    headers = {
        'Accept': '*/*',
        'X-Language': caches.lang,
        'X-Platform': os,
        'X-ClientVersion': code,
        'Content-Type': 'application/json',
        'User-Agent': dua
    }
    data = {'sign': enc_sign}

    r = requests.put(url, data=json.dumps(data), headers=headers)
    return r.json()

# link with a facebook account via sign encrypted facebook ID & OAuth token
def facebookLink(ver, os, fb_id, fb_token, token, secret):
    if os == 'android':
        dua = caches.device_agent1
    else:
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/user/link/facebook'
        auth = crypto.mac(ver, token, secret, 'POST', '/user/link/facebook')
        code = config.gb_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts
        sign = {'facebook_id': str(fb_id),'facebook_token': str(fb_token)}
    else:
        url = config.jp_url + '/user/link/facebook'
        auth = crypto.mac(ver, token, secret, 'POST', '/user/link/facebook')
        code = config.jp_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts
        sign = {'facebook_id': str(fb_id),'facebook_token': str(fb_token)}

    enc_sign = crypto.encrypt_sign(ver, json.dumps(sign))

    headers = {
        'X-Platform': os,
        'X-Language': caches.lang,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Authorization': auth,
        'User-Agent': dua
    }
    data = {'sign': enc_sign}

    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

# unlink facebook account
def facebookUnlink(ver, os, token, secret):
    if os == 'android':
        dua = caches.device_agent1
    else:
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/user/link/facebook'
        auth = crypto.mac(ver, token, secret, 'DELETE', '/user/link/facebook')
        code = config.gb_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts
    else:
        url = config.jp_url + '/user/link/facebook'
        auth = crypto.mac(ver, token, secret, 'DELETE', '/user/link/facebook')
        code = config.jp_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts

    headers = {
        'X-Platform': os,
        'X-Language': caches.lang,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Authorization': auth,
        'User-Agent': dua
    }

    r = requests.delete(url, headers=headers)
    return r.json()

# get list of linked accounts
def links(ver, os, token, secret):
    if os == 'android':
        dua = caches.device_agent1
    else:
        dua = caches.device_agent2
    if ver == 'gb':
        url = config.gb_url + '/user/links'
        auth = crypto.mac(ver, token, secret, 'GET', '/user/links')
        code = config.gb_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts
    else:
        url = config.jp_url + '/user/links'
        auth = crypto.mac(ver, token, secret, 'GET', '/user/links')
        code = config.jp_code[str(os)]
        asset = caches.asset_ts
        db = caches.database_ts

    headers = {
        'X-Platform': os,
        'X-Language': caches.lang,
        'X-ClientVersion': code,
        'X-AssetVersion': asset,
        'X-DatabaseVersion': db,
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Authorization': auth,
        'User-Agent': dua
    }

    r = requests.get(url, headers=headers)
    return r.json()
