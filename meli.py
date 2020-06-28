#!/usr/bin/env python
'''
Modulo meli
---------------------------
Autor: Hernan Contigiani

Descripcion:
Clases que consumen, parsean y persisten la información
recolectadas de distintas APIs de MELI
'''

__author__ = "Hernan Contigiani"
__email__ = "hernan4790@gmail.com"
__version__ = "1.0.0"

import asyncio
import aiohttp
from aiohttp import ClientSession

debug_mode = False


def active_debug_mode():
    debug_mode = True
    print('Debug mode ON')


class ApiMeli():
    '''Virtual class for API Meli model'''

    def __init__(self, api_child_list=()):
        self.id = None
        self.api_child_list = []

        # TODO: Analizar una mejor forma de construir clases de forma
        # dinámica
        for api_name in api_child_list:
            dynamic_class = d[api_name]()
            self.api_child_list.append(dynamic_class)

        pass

    def setup(self, api_meli):
        # Virtual method for data persist
        return None

    async def fetch(self):
        # Virtual method for data persist
        return None

    def parse(self, resp):
        # Virtual method for data persist
        return None

    def persist(self):
        # Virtual method for data persist
        return None


class CategoryApi(ApiMeli):
    '''Category class for fetch categorias meli API'''
    def setup(self, api_meli):
        self.id = getattr(api_meli, 'category_id', '')

    async def fetch(self):
        '''Call Category Meli Api'''
        if(debug_mode is True):
            print('Fetch category id', self.id)

        await asyncio.sleep(1)

        print('Category fetch id end', self.id)

        return None

    def persist(self):
        # Virtual method for data persist
        return None

# TODO: Analizar una mejor forma de construir clases de forma
# dinámica
d = {"CategoryApi": CategoryApi}


class ItemApi(ApiMeli):
    '''Item class for fetch item meli API'''

    url = 'https://api.mercadolibre.com/items?ids='

    def __init__(self, api_child_list=()):
        super(ItemApi, self).__init__(api_child_list)

        # Inicializo las variables que capturares de la Api
        self.price = ''
        self.start_time = ''
        self.category_id = ''
        self.currency_id = ''
        self.seller_id = ''

    def setup(self, item_id):
        '''Setup item id'''
        self.id = item_id

    async def fetch(self):
        '''Call Item Meli Api'''
        if(debug_mode is True):
            print('Fetch Item id', self.id)

        if not self.id:
            if(debug_mode is True):
                print('Error: Empty id, class Item')
            return 1

        self.url += self.id

        async with aiohttp.ClientSession() as session2:
            async with session2.get(self.url) as response:
                resp = await response.json()

        if(self.parse(resp) != 0):
            if(debug_mode is True):
                print('Error: Parse error, id', self.id)
            return 1

        tasks = []

        for api_child in self.api_child_list:
            api_child.setup(self)
            tasks.append(api_child.fetch())

        await asyncio.gather(*tasks)

        await self.persist()

        return 0

    def parse(self, resp):
        if not resp:
            if(debug_mode is True):
                print('Error: Empty resp, id', self.id)
            return 1

        body = resp[0].get('body')
        if body is not None:
            self.price = body.get('price', '')
            self.start_time = body.get('start_time', '')
            self.category_id = body.get('category_id', '')
            self.currency_id = body.get('currency_id', '')
            self.seller_id = body.get('seller_id', '')
        else:
            if(debug_mode is True):
                print('Error: No body, id', self.id)
            return 1

        return 0

    def persist(self):
        '''Persit Item'''
        if(debug_mode is True):
            print('Persist Item id', self.id)

        return 1
