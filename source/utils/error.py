import os
import json
import re
from datetime import datetime

import config as config
import api.caches as caches
import api.ingame as ingame
import farming.fapro as farmbot
import utils.colors as colors
import utils.database as database
import utils.funcs as funcs

# errors = ['invalid_token', 'client_version/new_client_version_exists', 'oauth2_mac_rails/link_code_not_found', 'already_accepted_mission_rewards', 'act_is_not_enough', 'the_number_of_cards_must_be_less_than_or_equal_to_the_capacity', 'no_condition_to_try_the_quest_is_fulfilled', 'invalid_area_conditions_potential_releasable', 'active_record/record_not_found', 'invalid_only_card_quest_limitation_conditions', 'invalid_requiring_card_quest_limitation_conditions', 'z_battle_check_point_does_not_exist', 'invalid_only_element_quest_limitation_conditions', 'invalid_allowed_category_quest_limitation_conditions', 'invalid_requiring_element_quest_limitation_conditions', 'visited_count_of_the_quest_reaches_the_limit', 'oauth2_mac_rails/client_transferred', 'act_is_already_maximum', 'already_linked_facebook_by_others', 'user_comeback_campaign_is_not_found', 'max_act_is_not_enough', 'special_item_is_not_enough', 'blank', 'card_unique_info_ids_must_be_unique', 'no_method_error', 'boost_point_is_not_enough', 'can_not_boost_not_cleared_sugoroku_map', 'invalid_client', 'cannot_draw_the_gasha', 'not_found_linked_facebook', 'not_exist_supporter_caches', 'total_cost_of_cards_must_be_less_than_or_equal_to_the_capacity', 'client_database/new_version_exists', 'client_assets/new_version_exists', 'contains_unteamable_card']
dir_path = os.path.dirname(os.path.realpath(__file__))
errors = json.loads(open(dir_path + '/' + 'errors.json', 'r').read())

def handler(source, response, stage=None, difficulty=None, kagi=None, return_drops=None, boost=False):
    global errors
    if 'error' in response:
        if 'code' in response['error']:
            if 'title' in response['error']:
                if 'description' in response['error'] and response['error']['description'] != '':
                    desc = str(response['error']['description']) + '\n' + str(response['error']['code'])
                else:
                    desc = str(response['error']['code'])
                if 'until' in response['error'] and response['error']['until'] != '':
                    ends_at = '\nEnds: ' + datetime.utcfromtimestamp(int(response['error']['until'])).strftime(
                        '%m/%d/%Y %H:%M.%S')
                else:
                    ends_at = ''
                print(colors.render('{error}[' + str(caches.acc_ver).upper() + '] ' + response['error'][
                    'title'] + '\n' + desc + ends_at))
                if caches.acc_ver == 'gb':
                    config.gb_maint = True
                else:
                    config.jp_maint = True
            elif str(response['error']['code']) in errors.keys():
                error_message = errors[str(response['error']['code'])]
                for match in re.findall(r'\\x[0-9A-Fa-f]{2}', error_message):
                    error_message = error_message.replace(match, chr(int(match[2:], 16)))
                print(colors.render('{error}[!] ' + str(error_message)))
                # refill stamina accordingly.
                if response['error']['code'] == 'act_is_not_enough':
                    store = ingame.user(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, False)
                    if 'error' not in store:
                        user = store['user']
                        required_act = database.fetch(caches.acc_ver + '.db', 'sugoroku_maps', 'quest_id=' + str(stage))
                        if int(required_act[7]) > int(user['act_max']):
                            print(colors.render('{error}Max stamina not enough to run this stage.'))
                        else:
                            stam_refill = farmbot.restore()
                            if stam_refill:
                                farmbot.handler(0, stage, difficulty, kagi, return_drops, boost)
                    else:
                        handler('stamUsr', store)
                # sell useless in box accordingly.
                if response['error']['code'] == 'the_number_of_cards_must_be_less_than_or_equal_to_the_capacity':
                    settings = funcs.get_settings()
                    if settings['autosell']:
                        if farmbot.sell_useless():
                            if settings['baba_useless']:
                                farmbot.baba_useless()
                            farmbot.handler(0, stage, difficulty, kagi, return_drops, boost)
                        else:
                            print(colors.render('{error}unable to sell.'))
                if response['error']['code'] == 'active_record/record_not_found':
                    caches.update_events()
            else:
                print(colors.render(str(source) + ' > error occurred:'))
                print(colors.render(
                    '{error}[!] "' + str(response) + '"\nPlease send a screenshot of this error to the Discord.'))
        else:
            if str(response['error']) in errors.keys():
                error_message = errors[str(response['error'])]
                for match in re.findall(r'\\x[0-9A-Fa-f]{2}', error_message):
                    error_message = error_message.replace(match, chr(int(match[2:], 16)))
                print(colors.render('{error}[!] ' + str(error_message)))
                # refresh session accordingly.
                if 'invalid_token' in response['error']:
                    funcs.refresh()
            else:
                print(colors.render(str(source) + ' > error occurred:'))
                print(colors.render(
                    '{error}"' + str(response) + '"\nPlease send a screenshot of this error to the Discord.'))
