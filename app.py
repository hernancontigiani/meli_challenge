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


async def main():

    api_child_list = ('CategoryApi','CategoryApi')

    item_1 = meli.ItemApi(api_child_list)
    item_2 = meli.ItemApi()

    item_1.setup('i1')
    item_2.setup('i2')

    tasks = []
        # for url in urls:
        #     tasks.append(
        #         write_one(file=file, url=url, session=session, **kwargs)
        #     )

    tasks.append(item_1.fetch())
    tasks.append(item_2.fetch())

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # Start api
    asyncio.run(main())  
