import json
import config as config
import api.caches as caches
import api.ingame as ingame
import utils.colors as colors
import utils.database as database
import utils.error as error
import utils.funcs as funcs

# TODO pluck units more accurate to the conditions
def build(limits, cards, stage):
    settings = funcs.get_settings()
    friend = cards[0]['id']
    friend_card = cards[0]['leader']['card_id']
    condits = ['forbid_card_ids', 'only_elements', 'requiring_elements', 'allowed_category_ids', 'only_card_ids']
    plucked = []
    print(colors.render('{message}[!] Building team...'))

    box = caches.cards

    decks = caches.teams
    plucked = []

    statues = config.x0a4_0

    '''
    717
    (3) only dbs movie characters - kid broly on your team - vegeta kid - 402&407 - 403&408 - 404&409 (only_card_ids) (requiring_card_ids)x2
    '''
    if len(str(stage)) == 6 and str(str(stage)[0:3]) == '712':
        for i in cards:
            if i['is_friend']:
                friend = i['id']
                friend_card = i['leader']['card_id']
                break
    else:
        for i in cards:
            friend = i['id']
            friend_card = i['leader']['card_id']
            break
    for j in limits:
        for x in j['conditions'].keys():
            if x in condits:
                if x == 'forbid_card_ids':
                    # 711 & 192
                    for i in cards:
                        if i['leader']['card_id'] not in j['conditions']['forbid_card_ids']:
                            friend = i['id']
                            friend_card = i['leader']['card_id']
                            break
                        else:
                            continue
                    for i in box:
                        card = json.dumps(i[3])
                        if i[1] not in j['conditions']['forbid_card_ids'] and str(i[1]) not in statues:
                            if len(plucked) < 1:
                                plucked.append(int(i[0]))
                            else:
                                break
                        else:
                            continue
                if x == 'only_card_ids':
                    if str(stage)[0:3] == '601' or str(stage)[0:3] == '603' or str(stage)[0:3] == '606':
                        for i in cards:
                            if i['leader']['card_id'] in j['conditions']['only_card_ids']:
                                friend = i['id']
                                friend_card = i['leader']['card_id']
                                break
                            else:
                                continue
                        for i in box:
                            if i[1] in j['conditions']['only_card_ids'] and str(i[1]) not in statues:
                                if len(plucked) < 1:
                                    plucked.append(int(i[0]))
                                else:
                                    break
                            else:
                                continue
                if x == 'only_elements':
                    # SBR mono
                    if int(j['id']) in [164, 166, 168, 170, 172, 174, 176, 178, 180, 182]:
                        elements = j['conditions']['only_elements']
                        for i in box:
                            if int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[13]) == int(elements[0]) and str(i[1]) not in statues:
                                if len(plucked) < 1:
                                    plucked.append(int(i[0]))
                                else:
                                    break
                            else:
                                continue
                    # z-awaken only
                    if int(j['id']) in [55, 56, 57, 58, 59, 60, 61, 62]:
                        elements = j['conditions']['only_elements']
                        elements.remove(0)
                        elements.remove(1)
                        elements.remove(2)
                        elements.remove(3)
                        elements.remove(4)
                        for i in box:
                            for e in elements:
                                if len(plucked) < 1:
                                    if int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[13]) == int(e) and int(i[0]) not in plucked and int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[6]) < 4 and database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[5] != str(int(i[1]) + 1) and str(i[1]) not in statues:
                                        plucked.append(int(i[0]))
                                    else:
                                        continue
                                else:
                                    break
                    # z-awaken excludes a type
                    if int(j['id']) in [43, 44, 45, 46, 47] or int(j['id']) in [75, 76, 77, 78, 79]:
                        elements = j['conditions']['only_elements']
                        for i in box:
                            for e in elements:
                                if len(plucked) < len(elements):
                                    if int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[
                                               13]) == int(e) and int(i[0]) not in plucked and int(
                                            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[
                                                6]) < 4 and \
                                            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[
                                                5] != str(int(i[1]) + 1) and str(i[1]) not in statues:
                                        plucked.append(int(i[0]))
                                    else:
                                        continue
                                else:
                                    break
                if x == 'requiring_elements':
                    # rainbow z-awaken
                    if int(j['id']) in [48, 49, 50, 51, 52, 53, 54, 110, 111, 112] or int(j['id']) in [80, 81, 82, 83, 84, 85, 86, 101, 102, 103, 137]:
                        elements = j['conditions']['requiring_elements']
                        already_picked = [] # farm medal 320022 2 3 30004
                        '''for i in cards:
                            for e in elements:
                                if int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i['leader']['card_id']))[13]) == int(e) and int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i['leader']['card_id']))[6]) < 4 and database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i['leader']['card_id']))[5] != str(int(i['leader']['card_id']) + 1) and e not in already_picked:
                                    friend = i['id']
                                    friend_card = i['leader']['card_id']
                                    print(str(i['leader']['card_id']) + ' - ' + str(e))
                                    break'''
                        for i in box:
                            for e in elements:
                                if len(plucked) < len(elements):
                                    if int(database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[
                                               13]) == int(e) and int(i[0]) not in plucked and int(
                                        database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[
                                            6]) < 4 and \
                                            database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[
                                                5] != str(int(i[1]) + 1) and e not in already_picked and str(i[1]) not in statues:
                                        plucked.append(int(i[0]))
                                        already_picked.append(e)
                                        #print(str(i['card_id']) + ' - ' + str(e))
                                else:
                                    break
                    # SBR mono class z-awaken (unsure if z-awaken check is necessary)
                    if int(j['id']) in [198, 201]:
                        elements = j['conditions']['requiring_elements']
                        for i in box:
                            if database.fetch(caches.acc_ver + '.db', 'cards', 'id=' + str(i[1]))[13] in elements and str(i[1]) not in statues:
                                if len(plucked) < 1:
                                    plucked.append(int(i[0]))
                                else:
                                    break
                            else:
                                continue
                if x == 'allowed_category_ids':
                    # SBR cats
                    cats = j['conditions']['allowed_category_ids']
                    for i in box:
                        # loop thro all cats on a single unit~
                        for k in database.fetchAll(caches.acc_ver + '.db', 'card_card_categories', 'card_id=' + str(i[1])):
                            if int(k[2]) == cats and str(i[1]) not in statues:
                                if len(plucked) < 1:
                                    plucked.append(int(i[0]))
                                else:
                                    break
                            else:
                                continue
    if len(plucked) != 0 and len(plucked) <= 6:
        while len(plucked) < 6:
            plucked.append(0)
        new_deck = {'num': 1, 'user_card_ids': plucked}
        decks['user_card_teams'].remove(decks['user_card_teams'][0])
        print(decks['user_card_teams'])
        decks['user_card_teams'].insert(0, new_deck)
        print(decks['user_card_teams'])
        if settings['dev_mode']:
            print(new_deck)
        store = ingame.set_team(caches.acc_ver, caches.acc_os, caches.sess_token, caches.sess_secret, '1', decks['user_card_teams'])
        if 'error' not in store:
            caches.teams = store
            print(colors.render('{success}Team built - deck #1'))
            return [friend, friend_card]
        else:
            error.handler('tb set1', store)
            return [None, None]
    else:
        return [friend, friend_card]
