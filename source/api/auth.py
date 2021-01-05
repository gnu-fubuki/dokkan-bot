import requests
import json
import config as config
import api.caches as caches
import utils.crypto as crypto

'''
    The default quota (per project) for calling the SafetyNet Attestation API is 10,000 requests per day.
    (this quota can be increased but it has to be requested before deploying the app.)
    - https://developer.android.com/training/safetynet/attestation

    i discovered that if SafetyNet quota is reached then the result becomes "failed"
    this can be used to bypass the SafetyNet "device_token" that people had a hard time trying to forge.
    currently as of 4.12.0 akatsuki is using this to collect analytics & stop root/jailbreak.
    "failed" cannot be subjected to a ban wave as it is just a result of SafetyNet...
    this result is not a dead giveaway to "tampered" devices. - k1mpl0s
'''


def register(ver, os, ad = None, unique = None, key = None):
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
        url = config.gb_url + '/auth/sign_up'
        code = config.gb_code[str(os)]
    else:
        url = config.jp_url + '/auth/sign_up'
        code = config.jp_code[str(os)]
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-Language': caches.lang,
        'User-Agent': dua
        }
    data = None
    acc_ad = None
    acc_unique = None
    if ad and unique and key:
        if ver == 'gb':
            user_acc = {
                'ad_id': ad,
                'country': caches.country,
                'currency': caches.currency,
                'device': dn,
                'device_model': dm,
                'os_version': dv,
                'platform': os,
                'unique_id': unique
            }
        else:
            user_acc = {
                'device': dn,
                'device_model': dm,
                'os_version': dv,
                'platform': os,
                'unique_id': unique
            }
        data = {'captcha_session_key': key, 'user_account': user_acc}
    else:
        unique = crypto.guid()
        acc_ad = unique[0]
        acc_unique = unique[1]
        if os == 'ios':
            acc_unique = str(str(acc_unique).split(':')[0]).upper()
        if ver == 'gb':
            user_acc = {
                'ad_id': acc_ad,
                'country': caches.country,
                'currency': caches.currency,
                'device': dn,
                'device_model': dm,
                'os_version': dv,
                'platform': os,
                'unique_id': acc_unique
            }
        else:
            user_acc = {
                'device': dn,
                'device_model': dm,
                'os_version': dv,
                'platform': os,
                'unique_id': acc_unique
            }
        data = {'device_token': config.x0a1_0[4], 'user_account': user_acc}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return [r.json(), acc_ad, acc_unique]


def login(ver, os, basic, first, key=None):
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
        url = config.gb_url + '/auth/sign_in'
        if first:
            code = config.gb_code[str(os)]
        else:
            code = config.gb_code[str(os)]
    else:
        url = config.jp_url + '/auth/sign_in'
        if first:
            code = config.jp_code[str(os)]
        else:
            code = config.jp_code[str(os)]
    headers = {
        'Accept': '*/*',
        'Authorization': 'Basic ' + str(basic),
        'Content-Type': 'application/json',
        'X-UserCountry': caches.country,
        'X-UserCurrency': caches.currency,
        'X-Platform': os,
        'X-ClientVersion': code,
        'X-Language': caches.lang,
        'User-Agent': dua
    }
    acc_unique = caches.uuid
    if os == 'ios':
        acc_unique = str(str(caches.uuid).split(':')[0]).upper()
    user_acc = {
        'device': dn,
        'device_model': dm,
        'os_version': dv,
        'platform': os,
        'unique_id': acc_unique
    }
    if key:
        data = {'captcha_session_key': key, 'user_account': user_acc}
    else:
        data = {'device_token': config.x0a1_0[4], 'user_account': user_acc}
    '''if key:
        data = {'captcha_session_key': key, 'ad_id': caches.ad, 'unique_id': caches.uuid}
    else:
        data = {'ad_id': caches.ad, 'unique_id': caches.uuid}'''
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()
