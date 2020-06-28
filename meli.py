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


class ApiMeli():
    """Virtual class for API Meli model"""

    def __init__(self, api_child_list = ()):
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

    def persist(self):
        # Virtual method for data persist
        return None


class CategoryApi(ApiMeli):
    """Category class for fetch categorias meli API"""
    def setup(self, api_meli):
        self.id = getattr(api_meli, 'category_id', '')


    async def fetch(self):
        
        print('Category fetch id start',self.id)

        await asyncio.sleep(1)

        print('Category fetch id end',self.id)


        return None

    def persist(self):
        # Virtual method for data persist
        return None

# TODO: Analizar una mejor forma de construir clases de forma
# dinámica
d = {"CategoryApi": CategoryApi}

class ItemApi(ApiMeli):
    """Item class for fetch item meli API"""
    def __init__(self, api_child_list = ()):
        super(ItemApi, self).__init__(api_child_list)
        self.category_id = None


    def setup(self, item_id):
        self.id = item_id
        self.category_id = 'c' + item_id


    async def fetch(self):
        
        print('Item fetch id start',self.id)

        tasks = []

        for api_child in self.api_child_list:
            api_child.setup(self)
            tasks.append(api_child.fetch())    

        await asyncio.gather(*tasks)

        print('Item fetch id end',self.id)

        return None

    def persist(self):
        # Virtual method for data persist
        return None

    