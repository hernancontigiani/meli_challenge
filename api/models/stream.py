#!/usr/bin/env python
'''
Modulo stream
---------------------------
Autor: Hernan Contigiani

Descripcion:
Modulo que contiene los diferentes tipos de
stream que soporta el sistema
'''

__author__ = "Hernan Contigiani"
__email__ = "hernan4790@gmail.com"
__version__ = "1.0.0"

import csv
import json


class Stream():
    '''Virtual class for Stream model'''
    def __init__(self, config):
        self.id = None
        self.is_open = False
        self.delimiter = config.get('delimiter', ',')
        self.encoding = config.get('encoding', 'utf-8')

    def open(self, file_name):
        try:
            self.fd = open(file_name, 'r', encoding=self.encoding)
            self.is_open = True
        except:
            self.is_open = False

    def close(self):
        if self.is_open is True:
            self.fd.close()
            self.is_open = False

    def get_chunk(self, chunksize):
        # Virtual method
        raise NotImplementedError

    def parse_line(self, line):
        # Virtual method
        raise NotImplementedError


class CsvStream(Stream):
    '''Class for CSV stream'''
    def __init__(self, config):
        super(CsvStream, self).__init__(config)
        self.reader = None

    def get_chunk(self, chunksize):
        chunk = []
        if self.is_open is False:
            return chunk

        if self.reader is None:
            self.reader = csv.DictReader(self.fd, delimiter=self.delimiter)

        for i in range(chunksize):
            row = next(self.reader, None)
            if row is None:
                break
            chunk.append(row)

        return chunk

    def parse_line(self, line):
        id_line = line.get('id')
        id = 0

        if isinstance(id_line, int):
            id = id_line
        elif isinstance(id_line, str):
            if id_line.isdigit() is True:
                id = int(id_line)

        site = line.get('site')
        return({'site': site, 'id': id})


class TxtStream(Stream):
    '''Class for TxT stream'''
    def __init__(self, config):
        super(TxtStream, self).__init__(config)

    def get_chunk(self, chunksize):
        chunk = []
        if self.is_open is False:
            return chunk

        for i in range(chunksize):
            row = self.fd.readline()
            if row is None:
                break
            chunk.append(row)

        return chunk

    def parse_line(self, line):
        data = line.split(self.delimiter)
        if len(data) < 2:
            return {}

        site = data[0]
        if data[1].isdigit() is True:
            id = int(data[1])
        else:
            id = 0
        return({'site': site, 'id': id})


class Jsonlstream(Stream):
    '''class for JSON Line stream'''
    def __init__(self, config):
        super(Jsonlstream, self).__init__(config)

    def get_chunk(self, chunksize):
        chunk = []
        if self.is_open is False:
            return chunk

        for i in range(chunksize):
            row = self.fd.readline()
            if row is None:
                break
            chunk.append(row)

        return chunk

    def parse_line(self, line):
        json1_str = line.replace('\n', '')
        json1_data = json.loads(json1_str)

        id = json1_data.get('id')
        site = json1_data.get('site')

        return({'site': site, 'id': id})

factory = {'CsvStream': CsvStream,
           'TxtStream': TxtStream,
           'Jsonlstream': Jsonlstream}
