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

import os

import asyncio
import psycopg2

from .app import app, read_file

from .models import meli
from .config import config

script_path = os.path.dirname(os.path.realpath(__file__))
config_path_name = os.path.join(script_path, 'config.ini')

db = config('db', config_path_name)
server_config = config('server', config_path_name)

schema_path_name = os.path.join(script_path, 'db')
schema_path_name = os.path.join(schema_path_name, db.get('schema', '*'))


def create_db():
    ''' Create database and scheme'''
    res = 0    # No error

    try:
        conn = psycopg2.connect(host=db['host'],
                                port=db['port'],
                                user=db['user'],
                                password=db['password'])
        cur = conn.cursor()

        cur.execute('END;')  # Workarround al problema de "autocommit"
        cur.execute('CREATE DATABASE {};'.format(db['database']))
        cur.execute(open(schema_path_name, "r").read())
        conn.commit()
        conn.close()
        create_schema()
    except:
        res = 1     # Database not created

    return res


def create_schema():
    conn = psycopg2.connect(host=db['host'],
                            port=db['port'],
                            user=db['user'],
                            password=db['password'])
    cur = conn.cursor()
    cur.execute(open(schema_path_name, "r").read())
    conn.commit()
    conn.close()


def main():
    try:
        conn = psycopg2.connect(host=db['host'],
                                port=db['port'],
                                user=db['user'],
                                password=db['password'],
                                database=db['database'])
        conn.close()
    except:
        print("First excecution, create db and schema")
        if(create_db() != 0):
            print('Critical error, no access to database', db['database'])
            quit()

    # Descomentar para habilitar los print
    # meli.active_debug_mode()
    meli.db = db

    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)

if __name__ == '__main__':
    # Run API server
    main()
