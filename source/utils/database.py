import requests
import sqlite3
from sqlite3 import Error
import os as fs
import time
import config as config
import api.outgame as outgame
import pysqlsimplecipher.decryptor as decryptor

def download(ver, os, token, secret, version, url):
    if ver == 'gb':
        x0a1_1 = config.x0a1_0[0].encode()
    else:
        x0a1_1 = config.x0a1_0[1].encode()
    print('downloading database... (this may take awhile.)')
    timer_start = int(round(time.time(), 0))
    #store = outgame.getDatabase(ver, os, token, secret)
    #url = store['url']
    r = requests.get(url, stream=True, allow_redirects=True)
    f = open('./data/enc_' + ver + '.db', 'wb')
    for chunk in r.iter_content(1024):
        f.write(chunk)
    f.close()
    timer_finish = int(round(time.time(), 0))
    timer_total = timer_finish - timer_start
    print(str(timer_total) + ' second(s) download.')
    print('decrypting... (this may take awhile.)')
    timer_start = int(round(time.time(), 0))
    decryptor.decrypt_file('./data/enc_' + ver + '.db', bytearray(x0a1_1), './data/' + ver + '.db')
    fs.unlink('./data/enc_' + ver + '.db')
    f = open('./data/' + ver + '-data.txt', 'w')
    f.write(str(version) + '\n')
    f.close()
    timer_finish = int(round(time.time(), 0))
    timer_total = timer_finish - timer_start
    print(str(timer_total) + ' second(s) decrypt.')

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def exec(db, query, values=None):
    con = sqlite3.connect(db)
    cur = con.cursor()
    if values is not None:
        #print(values)
        cur.execute(query, values)
    else:
        cur.execute(query)
    results = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return results

def query(db, table, where, amount):
    if db in ['gb.db', 'jp.db']:
        con = sqlite3.connect('./data/' + db)
    else:
        con = sqlite3.connect(db)
    cur = con.cursor()
    if where:
        query = "SELECT * FROM " + table + " WHERE " + where
    else:
        query = "SELECT * FROM " + table
    cur.execute(query)
    if amount == 0:
        results = cur.fetchone()
    else:
        results = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return results

def fetch(db, table, where):
    if fs.path.isfile('./data/gb.db'):
        query_result = query('gb.db', table, where, 0)
        if query_result is not None:
            return query('gb.db', table, where, 0)
        else:
            if fs.path.isfile('./data/jp.db'):
                return query('jp.db', table, where, 0)
    else:
        return query(db, table, where, 0)

def fetchAll(db, table, where):
    if fs.path.isfile('./data/gb.db'):
        query_result = query('gb.db', table, where, 1)
        if query_result is not None:
            return query('gb.db', table, where, 1)
        else:
            if fs.path.isfile('./data/jp.db'):
                return query('jp.db', table, where, 1)
    else:
        return query(db, table, where, 1)
