# Desafio Meli Api Scraping


Esta API permite consultar diferentes contenidos de MELI
y agruparlos y almacenarlos en una DB
- Leer los items por id y sitio provenientes de una archivo CSV, txt, jsonl.
- Consultar las APIs de categoria, moneda y usuario.
- Almacenar toda la información en una DB postgreSQL.
- Consultar a la base de datos por los items almacenados

## Dependencias
La API en cuestión corre en Python3 mediante el framework Flask.\
Otro modulo importante es el de aiohttp. Consultar el documento de dependencias para mayor informacion.\
NOTA: Como futura mejora se plantea utilizar docker para resolver el tema del deploy y las dependencias.

## Run
Para poder ejecutar la API necesitaremos descargar y ejecutar el docker de postgreSQL.\
En este caso por practicidad y experiencia previa se utilizó postgreSQL 9.6:

Instalar Docker
[Docker](https://docs.docker.com/engine/install/)

Descargar postgres:9.6 y ejecutar el servicio:

<pre><code>
sudo docker pull postgres:9.6
sudo docker run --name postgres96 -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres:9.6
</code></pre>

NOTA: Pueden colocar el user:password que desee, luego actualice los campos del archivo config.ini

## Uso Basico
#### 1. Configuración
Editar el archivo __config.ini__ según los parámetros deseados de lanzamiento, como por ejemplo:
- archivo con la información de los "items" a consumir (formato, encoding, delimitador, etc)
- configuración de la DB
- configuración de la ejecución de las corrutinas
#### 2. Levante el servicio
<pre><code>
$ cd meli_scraping   # dirigirse a la carpeta del proyecto
$ python3 -m api.server # lanzar el server (por default 127.0.0.1:5000)
</code></pre>
#### 3. Load items
Llamando al `/fileread` endpoint el sistema consumirá el archivo indicado e informará al usuario el tiempo de ejecución.\
Al finalizar se habrá cargado toda la información en la base de datos
#### 4. Leer base de datos de items
Llamando al `/items` endpoint estaremos solicitando al sistema que lea toda la base de datos de items y la imprima en pantalla en un formato tipo "json".\
Llamando al `/items/table` endpoint estaremos solicitando al sistema toda la base de datos pero se presentará la información en una tabla html.\
Estos endpoint soportan que se especifique el "limit" y "offset" con los cuales queremos que se consulte a la base de datos, ejemplo:\
http://127.0.0.1:5000/items/table?limit=10&offset=50

## Capturas
#### Index
![Inove banner](/images/index.png)
#### Items
![Inove banner](/images/items.png)
#### Items en tabla
![Inove banner](/images/items_table.png)

## Documentation
- [API](/doc/API.md)