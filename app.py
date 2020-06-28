#!/usr/bin/env python
'''
Modulo meli
---------------------------
Autor: Hernan Contigiani
 
Descripcion:
Flask API Rest que consume diferentes APIs de mercadolibre
por item id
'''

__author__ = "Hernan Contigiani"
__email__ = "hernan4790@gmail.com"
__version__ = "1.0.0"

import asyncio
import psycopg2

import meli
from config import config

db = config('postgresql')
meli_config = config('meli')
file_stream_config = config('filestream')


def create_db():
    ''' Create database and scheme'''
    res = 0    # No error

    try:
        conn = psycopg2.connect(host=db['host'], port = db['port'], user=db['user'], password=db['password'])
        cur = conn.cursor()

        cur.execute('END;')  # Workarround al problema de "autocommit"
        cur.execute('CREATE DATABASE {};'.format(db['database']))
        cur.execute(open("schema.sql", "r").read())
        conn.commit()
        conn.close()
    except:
        res = 1     # Database not created
    
    return res

if __name__ == '__main__':

    try:
        conn = psycopg2.connect(host=db['host'], port = db['port'], user=db['user'], password=db['password'], database=db['database'])
        cur = conn.cursor()
        conn.close()
    except:
        print("First excecution, create db and schema")
        if(create_db() != 0):
            print('Critical error, no access to database', db['database'])
            quit()


    meli.active_debug_mode()
    meli.db = db

    print('Init table:\n', meli.ItemApi.get_db())

    meli.ItemApi.clear_db()

    print('clear table:\n', meli.ItemApi.get_db())

    api_child_call_list = meli_config['api_item_call'].split(',')
    api_meli_list = []

    item_1 = meli.ItemApi(api_child_call_list)
    item_2 = meli.ItemApi()

    item_1.setup({'site': 'MLA', 'id': 845041373})
    item_2.setup({'site': 'MLA', 'id': 750925229})

    api_meli_list.append(item_1)
    api_meli_list.append(item_2)

    meli.async_load(api_meli_list)

    print('Finish table:\n', meli.ItemApi.get_db())
