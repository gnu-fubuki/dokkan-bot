import time
import os
import json
import api.ingame as ingame
import utils.funcs as funcs
import utils.error as error
import utils.database as database

# account defaults
'''lang = {'gb': 'en','jp': 'jp'}
country = {'gb': 'US', 'jp': 'JP'}
currency = {'gb': 'USD', 'jp': 'JPY'}'''
lang = 'en'
country = 'US'
currency = 'USD'
uuid = '0f97df48-01e3-4d8f-8ba0-a1e8cced278c:5bf18553fe25d277'
ad = '95c27e08-72bb-4760-83e8-9e878d1999f8'

# android User-Agent
device_name1 = 'SM'
device_model1 = 'SM-S10'
device_ver1 = '9.0'
device_agent1 = 'Dalvik/2.1.0 (Linux; Android 9.0; SM-S10)'
# ios User-Agent
device_name2 = 'iPhone'
device_model2 = 'iPhone XR'
device_ver2 = '13.0'
device_agent2 = 'CFNetwork/808.3 Darwin/16.3.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X)'

# cached account config
loaded = None  # save file
account = ''  # identifier
acc_os = ''  # platform
acc_ver = ''  # game version
sess_token = ''  # session token
sess_secret = ''  # session secret

# client data
database_ts = str(int(round(time.time(), 0)))
asset_ts = None

file_ts1 = str(int(round(time.time(), 0)))
file_ts2 = str(int(round(time.time(), 0)))
db_ts1 = str(int(round(time.time(), 0)))
db_ts2 = str(int(round(time.time(), 0)))

# store account information
teams = None
support_leader = 0
cards = []
item_cards = []
events = {}

def assign_cards():
    global loaded
    global cards
    global item_cards
    cards = database.query(f"./boxes/{loaded}.db", 'cards', None, 1)
    item_cards = database.query(f"./boxes/{loaded}.db", 'item_cards', None, 1)
    return True


def card_pool(card):
    global loaded
    query = database.query(f"./boxes/{loaded}.db", 'drops', 'unique_id=' + str(card), 0)
    if query is None:
        database.exec(f"./boxes/{loaded}.db", f"INSERT INTO drops(unique_id, test) VALUES (?, ?)", (int(card), 0))


def remove_cards(input_cards, input_items):
    global loaded
    test = []
    for i in input_cards:
        test.append(i['id'])
    #print(test)
    #print(len(test))
    if input_cards is None:
        input_cards = []
    if input_items is None:
        input_items = []
    for i in input_cards:
        query = database.query(f"./boxes/{loaded}.db", 'cards', 'id=' + str(i['id']), 0)
        if query is not None:
            database.exec(f"./boxes/{loaded}.db", "DELETE FROM cards where id=?", [int(i['id'])])
        query = database.query(f"./boxes/{loaded}.db", 'drops', 'unique_id=' + str(i['id']), 0)
        if query is not None:
            database.exec(f"./boxes/{loaded}.db", "DELETE FROM drops where unique_id=?", [int(i['id'])])
    for i in input_items:
        query = database.query(f"./boxes/{loaded}.db", 'item_cards', 'card_id=' + str(i['card_id']), 0)
        if query is not None:
            if i['quantity'] != 0:
                database.exec(f"./boxes/{loaded}.db", "UPDATE item_cards SET quantity=? where card_id=?",
                              (int(query[1]) + int(i['quantity']), int(i['card_id'])))
            else:
                database.exec(f"./boxes/{loaded}.db", "DELETE FROM item_cards where card_id=?", [int(i['card_id'])])
    assign_cards()


def add_cards(input_cards, input_items):
    global loaded
    if input_cards is None:
        input_cards = []
    if input_items is None:
        input_items = []
    for i in input_cards:
        query = database.query(f"./boxes/{loaded}.db", 'cards', 'id=' + str(i['id']), 0)
        if query is None:
            database.exec(f"./boxes/{loaded}.db",
                          f"INSERT INTO cards(id, card_id, updated_at, serialized) VALUES (?, ?, ?, ?)",
                          (int(i['id']), int(i['card_id']), int(i['updated_at']), str(json.dumps(i))))
    for i in input_items:
        query = database.query(f"./boxes/{loaded}.db", 'item_cards', 'card_id=' + str(i['card_id']), 0)
        if query is None:
            if i['quantity'] != 0:
                database.exec(f"./boxes/{loaded}.db", f"INSERT INTO item_cards(card_id, quantity) VALUES (?, ?)",
                              (int(i['card_id']), int(i['quantity'])))
        else:
            update_cards(None, input_items)
    assign_cards()


def update_cards(input_cards, input_items):
    global loaded
    if input_cards is None:
        input_cards = []
    if input_items is None:
        input_items = []
    for i in input_cards:
        query = database.query(f"./boxes/{loaded}.db", 'cards', 'id=' + str(i['id']), 0)
        if query is not None:
            database.exec(f"./boxes/{loaded}.db", "UPDATE cards SET updated_at=?, serialized=? where id=?",
                          (int(i['updated_at']), str(json.dumps(i)), int(i['id'])))
    for i in input_items:
        query = database.query(f"./boxes/{loaded}.db", 'item_cards', 'card_id=' + str(i['card_id']), 0)
        if query is not None:
            if i['quantity'] != 0:
                database.exec(f"./boxes/{loaded}.db", "UPDATE item_cards SET quantity=? where card_id=?",
                              (int(query[1]) + int(i['quantity']), int(i['card_id'])))
    assign_cards()


def load_account(save, iden, par_ver, par_os, token, secret, show=False):
    global loaded
    global account
    global acc_ver
    global acc_os
    global sess_token
    global sess_secret
    global teams
    global support_leader
    global events
    loaded, account, acc_ver, acc_os, sess_token, sess_secret = save, iden, par_ver, par_os, token, secret
    if not os.path.isfile(f"./boxes/{loaded}.db"):
        database.create_connection(f"./boxes/{loaded}.db")
        database.exec(f"./boxes/{loaded}.db", "CREATE TABLE cards(id INTEGER PRIMARY KEY, card_id INTEGER, updated_at INTEGER, serialized TEXT NOT NULL)")
        database.exec(f"./boxes/{loaded}.db", "CREATE TABLE item_cards(card_id INTEGER PRIMARY KEY, quantity INTEGER)")
        database.exec(f"./boxes/{loaded}.db", "CREATE TABLE drops(unique_id INTEGER PRIMARY KEY, test INTEGER)")
    if funcs.check_database(acc_ver, acc_os, sess_token, sess_secret):
        funcs.check_asset()
        store = ingame.login_resources(acc_ver, acc_os, sess_token, sess_secret)
        if 'error' not in store:
            if 'teams' in store:
                teams = store['teams']
            if 'support_leaders' in store:
                if 'support_leader_ids' in store['support_leaders']:
                    if len(store['support_leaders']['support_leader_ids']) != 0:
                        support_leader = store['support_leaders']['support_leader_ids'][0]
            if 'cards' in store:
                add_cards(store['cards'], None)
            if 'item_cards' in store:
                add_cards(None, store['item_cards'])
        else:
            error.handler('resLeader', store)
        store = ingame.events(acc_ver, acc_os, sess_token, sess_secret)
        if 'error' not in store:
            events = store
        else:
            error.handler('errorLS', store)
        if show:
            funcs.navigator(99)
    else:
        loaded = None

def update_events():
    global acc_ver
    global acc_os
    global sess_token
    global sess_secret
    global events
    store = ingame.events(acc_ver, acc_os, sess_token, sess_secret)
    if 'error' not in store:
        events = store
    else:
        error.handler('errorLS', store)
