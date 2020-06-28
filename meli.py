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
import psycopg2
import aiohttp
from aiohttp import ClientSession

db = {}


class ApiMeli():
    '''Virtual class for API Meli model'''
    debug_mode = False

    @staticmethod
    def set_debug_mode(mode):
        ApiMeli.debug_mode = mode

    def __init__(self, api_child_list=()):
        self.id = None
        self.url = ''
        self.api_child_list = []

        for api_name in api_child_list:
            dynamic_class = factory[api_name]()
            self.api_child_list.append(dynamic_class)

    async def load(self):
        '''Load Meli Api'''
        if(self.debug_mode is True):
            print('Load', self.__class__.__name__, 'id', self.id)

        if not self.id:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__, ': empty id')
            return 1

        await self.fetch()

        # Load child API calls
        tasks = []

        for api_child in self.api_child_list:
            api_child.setup(self)
            tasks.append(api_child.load())

        await asyncio.gather(*tasks)

        for api_child in self.api_child_list:
            api_child.decorate(self)

        await self.persist()

        return 0

    async def fetch(self):
        '''Fetch Item Meli Api'''
        if(self.debug_mode is True):
            print('Fetch', self.__class__.__name__, ': id', self.id)

        async with aiohttp.ClientSession() as session2:
            async with session2.get(self.url) as response:
                resp = await response.json()

        if(self.parse(resp) != 0):
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': Parse error, id', self.id)
            return 1

        return 0

    def setup(self, api_meli):
        # Virtual method
        raise NotImplementedError

    def parse(self, resp):
        # Virtual method
        raise NotImplementedError

    def decorate(self, resp):
        # Virtual method
        raise NotImplementedError

    async def persist(self):
        # Virtual method
        raise NotImplementedError


class CategoryApi(ApiMeli):
    '''Category class for fetch categorias meli API'''
    def __init__(self, api_child_list=()):
        super(CategoryApi, self).__init__(api_child_list)

        # Inicializo las variables que captura de la Api
        self.name = ''

    def setup(self, api_meli):
        self.id = getattr(api_meli, 'category_id', '')
        self.url = 'https://api.mercadolibre.com/categories/{}'.format(self.id)

    def parse(self, resp):
        if not resp:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': Empty resp, id', self.id)
            return 1

        self.name = resp.get('name', '')

        return 0

    def decorate(self, api_meli):
        setattr(api_meli, 'category_name', self.name)

    async def persist(self):
        '''Persit model to DB'''
        if(self.debug_mode is True):
            print('Persist', self.__class__.__name__,
                  ': id', self.id)

        if not db:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': not db, id', self.id)
            return 1

        return 1


class CurrencyApi(ApiMeli):
    '''Category class for fetch currency meli API'''
    def __init__(self, api_child_list=()):
        super(CurrencyApi, self).__init__(api_child_list)

        # Inicializo las variables que captura de la Api
        self.description = ''

    def setup(self, api_meli):
        self.id = getattr(api_meli, 'currency_id', '')
        self.url = 'https://api.mercadolibre.com/currencies/{}'.format(self.id)

    def parse(self, resp):
        if not resp:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': Empty resp, id', self.id)
            return 1

        self.description = resp.get('description', '')

        return 0

    def decorate(self, api_meli):
        setattr(api_meli, 'currency_description', self.description)

    async def persist(self):
        '''Persit model to DB'''
        if(self.debug_mode is True):
            print('Persist', self.__class__.__name__,
                  ': id', self.id)

        if not db:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': not db, id', self.id)
            return 1

        return 1

# TODO: Implementar factory
factory = {'CategoryApi': CategoryApi, 'CurrencyApi': CurrencyApi}


class ItemApi(ApiMeli):
    '''Item class for fetch item meli API'''
    def __init__(self, api_child_list=()):
        super(ItemApi, self).__init__(api_child_list)

        # Inicializo las variables que captura de la Api
        self.site = ''
        self.price = ''
        self.start_time = ''
        self.category_id = ''
        self.category_name = ''
        self.currency_id = ''
        self.currency_description = ''
        self.seller_id = ''

    def setup(self, site_id):
        '''Setup item id'''
        self.id = site_id.get('id', '')
        self.site = site_id.get('site', '')
        self.url = 'https://api.mercadolibre.com/items? \
                    ids={}{}'.format(self.site, self.id)

    def parse(self, resp):
        if not resp:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': Empty resp, id', self.id)
            return 1

        body = resp[0].get('body')
        if body is not None:
            self.price = body.get('price', '')
            self.start_time = body.get('start_time', '')
            self.category_id = body.get('category_id', '')
            self.currency_id = body.get('currency_id', '')
            self.seller_id = body.get('seller_id', '')
        else:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': No body, id', self.id)
            return 1

        return 0

    async def persist(self):
        '''Persit model to DB'''
        if(self.debug_mode is True):
            print('Persist', self.__class__.__name__,
                  ': id', self.id)

        if not db:
            if(self.debug_mode is True):
                print('Error', self.__class__.__name__,
                      ': not db, id', self.id)
            return 1

        conn = psycopg2.connect(host=db['host'], port=db['port'],
                                user=db['user'], password=db['password'],
                                database=db['database'])
        cur = conn.cursor()

        query = "INSERT INTO items(id,site,price,start_time,name,description,seller_id) \
                    VALUES ({},'{}','{}','{}','{}','{}','{}') \
                    ON CONFLICT (id) DO UPDATE SET price = '{}';".format(
                        self.id, self.site, self.price, self.start_time,
                        self.category_name, self.currency_description,
                        self.seller_id, self.price)

        query = query.replace("''", "null")
        cur.execute(query)

        conn.commit()
        conn.close()
        return 0

    @staticmethod
    def clear_db():
        conn = psycopg2.connect(host=db['host'], port=db['port'],
                                user=db['user'], password=db['password'],
                                database=db['database'])
        cur = conn.cursor()
        cur.execute('TRUNCATE items;')
        cur.execute('DELETE FROM items;')
        conn.commit()
        conn.close()

    @staticmethod
    def get_db(limit=0, offset=0):
        conn = psycopg2.connect(host=db['host'], port=db['port'],
                                user=db['user'], password=db['password'],
                                database=db['database'])
        cur = conn.cursor()

        query = 'SELECT * FROM items'

        if limit > 0:
            query += ' LIMIT{}'.format(limit)

        if offset > 0:
            query += ' OFFSET{}'.format(offset)

        query += ';'

        cur.execute(query)
        query_results = cur.fetchall()
        conn.close()
        return query_results


async def async_load_task(api_meli_list):
    tasks = []

    for api_meli in api_meli_list:
        tasks.append(api_meli.load())

    await asyncio.gather(*tasks)


def active_debug_mode():
    ApiMeli.set_debug_mode(True)
    print('Debug mode ON')


def async_load(api_meli_list):
    asyncio.run(async_load_task(api_meli_list))
