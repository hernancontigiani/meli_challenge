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
import json
import traceback

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

    file_path_name = os.path.join(script_path,
                                  file_stream_config.get('name', '*'))
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
            # print('from',count,'to',count+len(items))
            meli.async_load(items)
        else:
            break
        count += len(items)

    else:
        print("File note found")


@app.route("/")
def index():
    try:
        result = "<h1>Welcome!!</h1>"
        result += "<h2>Endpoints available:</h2>"
        result += "<h3>/fileread --> read the file based on configuration file</h3>"
        result += "<h3>/items?limit=?&offset=? --> show the items DB (limite and offset are optional)</h3>"
        result += "<h3>/items/table?limit=?&offset=? --> show the items DB in HTML tablet format(limite and offset are optional)</h3>"
        result += "<h3>/items/clear --> clear items DB</h3>"
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/fileread")
def file_read():
    try:
        time1 = time.time()
        read_file()
        time2 = time.time()
        result = 'done! elapsed time: {:.2f}s'.format(time2-time1)
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/items")
def show_items():
    try:
        return (show_db('json'))
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/items/table")
def show_table():
    try:
        return (show_db('table'))
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/items/clear")
def clear_items():
    try:
        meli.ItemApi.clear_db()
        result = "<h3>Items DB clear!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


def show_db(show_type='json'):

    limit_str = str(request.args.get('limit'))
    offset_str = str(request.args.get('offset'))

    limit = 0
    offset = 0

    if(limit_str is not None) and (limit_str.isdigit()):
        limit = int(limit_str)

    if(offset_str is not None) and (offset_str.isdigit()):
        offset = int(offset_str)

    data = meli.ItemApi.get_db(limit=limit, offset=offset)

    if show_type == 'json':
        return jsonify(data)
    elif show_type == 'table':
        return html_table(data)
    else:
        return jsonify(data)


def html_table(data):

    result = '<table border="1">'
    result += '<thead cellpadding="1.0" cellspacing="1.0">'
    result += '<tr>'
    result += '<th>Site</th>'
    result += '<th>Id</th>'
    result += '<th>Price</th>'
    result += '<th>Time</th>'
    result += '<th>Name</th>'
    result += '<th>Description</th>'
    result += '</tr>'

    for row in data:

        row = ['None' if v is None else v for v in row]

        result += '<tr>'
        result += '<td>' + str(row[0]) + '</td>'
        result += '<td>' + str(row[1]) + '</td>'
        result += '<td>' + str(row[2]) + '</td>'
        result += '<td>' + str(row[3]) + '</td>'
        result += '<td>' + str(row[4]) + '</td>'
        result += '<td>' + str(row[5]) + '</td>'
        result += '</tr>'

    result += '</thead cellpadding="0" cellspacing="0" >'
    result += '</table>'

    return result


