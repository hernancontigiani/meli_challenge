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
import time

import asyncio
import psycopg2
from flask import Flask, request, jsonify, Response

from .models import meli, stream
from .config import config

app = Flask(__name__)

script_path = os.path.dirname(os.path.realpath(__file__))
config_path_name = os.path.join(script_path, 'config.ini')

meli_config = config('meli', config_path_name)
file_stream_config = config('filestream', config_path_name)

def read_file():

    file_type = file_stream_config.get('type')
    stream_obj = stream.factory.get(file_type)(file_stream_config)

    file_path_name = os.path.join(script_path, file_stream_config.get('name', '*'))
    stream_obj.open(file_path_name)
    chunk_size = int(file_stream_config.get('chunk_size', '8'))

    api_child_call_list = meli_config['api_item_call'].split(',')

    count = 0

    while stream_obj.is_open is True:
        chunks = stream_obj.get_chunk(chunksize=chunk_size)
        items = []
        for chunk in chunks:
            site_id = stream_obj.parse_line(chunk)
            item = meli.ItemApi(api_child_call_list)
            item.setup(site_id)
            items.append(item)

        if len(items) > 0:
            print('from',count,'to',count+len(items))
            meli.async_load(items)
        else:
            break
        count += len(items)

    else:
        print("File note found")

    
@app.route("/")
def index():
    result = "<h1>Welcome!!</h1>"
    result += "<h2>Endpoints available:</h2>"
    result += "<h3>/fileread --> read the file based on configuration file</h3>"
    result += "<h3>/items?limit=?&offset=? --> show the items DB (limite and offset are optional</h3>"
    result += "<h3>/items/table?limit=?&offset=? --> show the items DB in HTML tablet format(limite and offset are optional</h3>"
    return(result)


@app.route("/fileread")
def file_read():
    time1 = time.time()
    read_file()
    time2 = time.time()
    result = 'done! elapsed time: {:.2f}s'.format(())
    return(result)