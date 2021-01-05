import ctypes
import platform
from cefpython3 import cefpython as cef
import requests
from urllib.parse import quote
import webbrowser
import api.auth as auth
import api.caches as caches
import api.transfer as transfer
import utils.crypto as crypto
import utils.colors as colors
import utils.error as error
import utils.funcs as funcs

app_id = None
package = None
par1 = []
facebook_id = None
session_secret = None
facebook_token = None

'''
Invoking the Login Dialog and Setting the Redirect URL

• client_id. The ID of your app, found in your app's dashboard.
• redirect_uri. The URL that you want to redirect the person logging in back to.
• state. A string value created by your app to maintain state between the request and callback.

https://developers.facebook.com/docs/facebook-login
https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
'''
def loginPage(ver):
    global app_id
    global package
    if ver == 'gb':
        app_id = '408947592639393'
        package = 'com.bandainamcogames.dbzdokkanww'
        state = '{"whitelist_redirect_url":"https:\/\/[*.-2\g].aktsk.com*\success","0_auth_logger_id":"1aaa277d-331a-4dec-8223-836e2318fd85","3_method":"web_view"}'
        url = 'https://m.facebook.com/v5.0/dialog/oauth?client_id=' + app_id + '&sdk=android-4.39.0&scope=public_profile&redirect_uri=fbconnect%3A%2F%2Fsuccess&state=' + quote(state) + '&auth_type=rerequest&display=touch&response_type=token&return_scopes=false&ret=login&fbapp_pres=0&logger_id=2dfa29d9-79c7-4d06-a5c2-836f21714483'
    else:
        app_id = '849869535146477'
        package = 'com.bandainamcogames.dbzdokkan'
        state = '{"whitelist_redirect_url":"https:\/\/[*.-2\g].aktsk.jp*\success","0_auth_logger_id":"2dfa29d9-79c7-4d06-a5c2-836f21714483","3_method":"web_view"}'
        url = 'https://m.facebook.com/v5.0/dialog/oauth?client_id=' + app_id + '&sdk=android-4.39.0&scope=public_profile&redirect_uri=fbconnect%3A%2F%2Fsuccess&state=' + quote(state) + '&auth_type=rerequest&display=touch&response_type=token&return_scopes=false&ret=login&fbapp_pres=0&logger_id=2dfa29d9-79c7-4d06-a5c2-836f21714483'
    return url

def webView(ver, os, url, which, t = None, s = None):
    global par1
    try:
        par1.append([ver, os, which, t, s])

        cef.Initialize()
        window_info = cef.WindowInfo()
        browser = cef.CreateBrowserSync(url=url, window_info=window_info, window_title='16 - Facebook transfer.')

        if platform.system() == 'Windows':
            window_handle = browser.GetOuterWindowHandle()
            insert_after_handle = 0
            SWP_NOMOVE = 0x0002
            ctypes.windll.user32.SetWindowPos(window_handle, insert_after_handle, 0, 0, 450, 500, SWP_NOMOVE)

        browser.SetClientHandler(LoadHandler())
        cef.MessageLoop()
    except:
        print(colors.render('{error}[cefpython3] something went wrong.'))


class LoadHandler(object):
    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):
        global par1
        global facebook_id
        global facebook_token
        if 'fbconnect://success' in failed_url:
            facebook_token = failed_url.replace('fbconnect://success#', '').split('&')[0].replace('access_token=', '')
            browser.CloseBrowser()
            del browser
            #ocef.Shutdown()
            url = 'https://graph.facebook.com/v3.2/me?access_token=' + str(facebook_token) + '&fields=name&format=json&sdk=android'
            headers = {
                'User-Agent': 'FBAndroidSDK.4.39.0',
                'Accept-Language': 'en_US',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Encoding': 'gzip',
                'Accept-Encoding': 'gzip'
            }
            r = requests.get(url=url, headers=headers)
            #print('cookie FB ID: ' + str(facebook_id))
            #print(r.json())
            facebook_id = r.json()['id']
            #print('OAuth FB ID: ' + str(facebook_id))
            #print('session secret: ' + str(session_secret))
            #print('OAuth token: ' + str(facebook_token))

            #print(par1)
            # validate
            if par1[0][2] == 0:
                print('[16] facebook validate')
                acc_ver, acc_os = par1[0][0], par1[0][1]
                store = transfer.facebookValidate(acc_ver, acc_os, facebook_id, facebook_token)
                if 'error' not in store:
                    if 'sign' in store:
                        store = crypto.decrypt_sign(caches.acc_ver, store['sign'])
                        print(store)
                    else:
                        error.handler('fb nosign', store)
                else:
                    error.handler('fb validate', store)
            # transfer
            if par1[0][2] == 1:
                print('[16] facebook transfer')
                acc_ver, acc_os = par1[0][0], par1[0][1]
                store = transfer.facebook(acc_ver, acc_os, facebook_id, facebook_token)
                if 'error' not in store:
                    store = crypto.decrypt_sign(acc_ver, store['sign'])
                    iden = store['identifiers'].replace('\n', '')
                    print(colors.render('{message}identifier for recover.\n' + iden))
                    store = auth.login(acc_ver, acc_os, crypto.basic(iden), False)
                    if 'error' not in store:
                        if 'reason' not in store:
                            save = funcs.create_save_file(acc_ver, acc_os, iden)
                            caches.load_account(save, iden, acc_ver, acc_os, store['access_token'], store['secret'], True)
                        else:
                            url = store['captcha_url']
                            key = store['captcha_session_key']
                            webbrowser.open(url, new=1, autoraise=True)
                            print('Complete CAPTCHA to login... Press ENTER when done.')
                            input()
                            store = auth.login(acc_ver, acc_os, crypto.basic(iden), False, key)
                            if 'error' not in store:
                                save = funcs.create_save_file(acc_ver, acc_os, iden)
                                caches.load_account(save, iden, acc_ver, acc_os, store['access_token'], store['secret'], True)
                            else:
                                error.handler('add login2', store)
                    else:
                        error.handler('add login', store)
                else:
                    error.handler('fb use', store)
            # link
            if par1[0][2] == 2:
                print('[16] facebook linking')
                acc_ver, acc_os = par1[0][0], par1[0][1]
                store = transfer.facebookLink(acc_ver, acc_os, facebook_id, facebook_token, par1[0][3], par1[0][4])
                if 'error' not in store:
                    if 'sign' in store:
                        store = crypto.decrypt_sign(acc_ver, store['sign'])
                        print(colors.render('{success}' + store['external_links']['facebook']))
                    else:
                        error.handler('fb no sign2', store)
                else:
                    error.handler('fb link', store)
            par1 = []
