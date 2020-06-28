#!/usr/bin/env python
'''
Modulo de test meli
---------------------------
Autor: Hernan Contigiani

Descripcion:
unit test del modulo meli
'''

__author__ = "Hernan Contigiani"
__email__ = "hernan4790@gmail.com"
__version__ = "1.0.0"

import unittest

import meli


class MeliTestCase(unittest.TestCase):
    ''' Ensayo de las APIs de meli'''
    def test_load(self):

        # Ensayo API items
        site_id = {'site': 'MLA', 'id': 845041373}
        item = meli.ItemApi()
        item.setup(site_id)

        meli.async_load([item])

        item_vars = vars(item)
        self.assertEqual(item_vars.get('id'), 845041373)
        self.assertEqual(item_vars.get('site'), 'MLA')
        self.assertEqual(item_vars.get('category_id'), 'MLA420226')
        self.assertEqual(item_vars.get('currency_id'), 'ARS')
        self.assertEqual(item_vars.get('seller_id'), 78528152)

        # Ensayo API categorias
        category = meli.CategoryApi()
        category.setup(item)
        meli.async_load([category])

        category_vars = vars(category)
        self.assertEqual(category_vars.get('id'), 'MLA420226')
        self.assertEqual(category_vars.get('name'), 'Displays y LCD')

        # Ensayo API currency
        currency = meli.CurrencyApi()
        currency.setup(item)
        meli.async_load([currency])

        currency_vars = vars(currency)
        self.assertEqual(currency_vars.get('id'), 'ARS')
        self.assertEqual(currency_vars.get('description'), 'Peso argentino')


if __name__ == '__main__':
    unittest.main()
