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

import meli


if __name__ == '__main__':

    meli.active_debug_mode()

    api_child_call_list = ('CategoryApi', 'CurrencyApi')
    api_meli_list = []

    item_1 = meli.ItemApi(api_child_call_list)
    item_2 = meli.ItemApi()
    item_3 = meli.ItemApi()

    item_1.setup('MLA845041373')
    item_2.setup('MLA2')
    item_3.setup('MLA3')

    api_meli_list.append(item_1)
    api_meli_list.append(item_2)
    api_meli_list.append(item_3)

    meli.async_load(api_meli_list)


    api_meli_list = []

    item_4 = meli.ItemApi(api_child_call_list)
    item_5 = meli.ItemApi()
    item_6 = meli.ItemApi()

    item_4.setup('MLA4')
    item_5.setup('MLA5')
    item_6.setup('MLA6')

    api_meli_list.append(item_4)
    api_meli_list.append(item_5)
    api_meli_list.append(item_6)

    meli.async_load(api_meli_list)

    print(vars(item_1))

