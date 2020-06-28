#!/usr/bin/env python
'''
Modulo de test stream
---------------------------
Autor: Hernan Contigiani

Descripcion:
unit test del modulo stream
'''

__author__ = "Hernan Contigiani"
__email__ = "hernan4790@gmail.com"
__version__ = "1.0.0"

import os
import unittest

from stream import CsvStream, TxtStream, Jsonlstream


script_path = os.path.dirname(os.path.realpath(__file__))
# Work arround para no perder tiempo con el detalle de los directorios
file_path = script_path.replace('models', '')

class StreamTestCase(unittest.TestCase):
    ''' Ensayo de los streams'''
    def test_get_chunk(self):

        # Test csv stream
        file_name = os.path.join(file_path, 'technical_challenge_data.csv')

        config = {'delimiter': ',', 'encoding': 'utf-8'}
        csv_stream = CsvStream(config)
        csv_stream.open(file_name)

        # Check chunk size
        chunksize = 2
        chunk = csv_stream.get_chunk(chunksize=chunksize)
        self.assertEqual(len(chunk), chunksize)

        # Test txt stream
        file_name = os.path.join(file_path, 'technical_challenge_data.txt')

        config = {'delimiter': '|', 'encoding': 'utf-8'}
        txt_stream = TxtStream(config)
        txt_stream.open(file_name)

        # Check chunk size
        chunksize = 2
        chunk = txt_stream.get_chunk(chunksize=chunksize)
        self.assertEqual(len(chunk), chunksize)

        # Jsonlstream
        file_name = os.path.join(file_path, 'technical_challenge_data.jsonl')

        config = {'delimiter': ',', 'encoding': 'utf-8'}
        jsonl_stream = Jsonlstream(config)
        jsonl_stream.open(file_name)

        # Check chunk size
        chunksize = 2
        chunk = jsonl_stream.get_chunk(chunksize=chunksize)
        self.assertEqual(len(chunk), chunksize)

    def test_parse_line(self):
        id_test = 905070
        site_test = 'MLA'
        dump = 'dump'

        # Test csv stream
        csv_dict_line = {'id': id_test, 'site': site_test, 'dump': dump}

        config = {'delimiter': ',', 'encoding': 'utf-8'}
        csv_stream = CsvStream(config)
        chunk = csv_stream.parse_line(csv_dict_line)

        self.assertEqual(chunk.get('id'), id_test)
        self.assertEqual(chunk.get('site'), site_test)

        # Test txt stream
        config = {'delimiter': '|', 'encoding': 'utf-8'}
        delimiter = config['delimiter']
        txtline = site_test + delimiter + str(id_test)

        txt_stream = TxtStream(config)
        chunk = txt_stream.parse_line(txtline)

        self.assertEqual(chunk.get('id'), id_test)
        self.assertEqual(chunk.get('site'), site_test)

        # Test jsonl stream
        config = {'delimiter': ',', 'encoding': 'utf-8'}
        # json_line = '{"site": "{}", "id": {}}\n'.format(site_test, id_test)
        json_line = '{"site": "MLA", "id": 905070}\n'

        jsonl_stream = Jsonlstream(config)
        chunk = jsonl_stream.parse_line(json_line)

        self.assertEqual(chunk.get('id'), id_test)
        self.assertEqual(chunk.get('site'), site_test)


if __name__ == '__main__':
    unittest.main()
