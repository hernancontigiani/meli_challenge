# Diseño
Este documento describe las consideración de diseño que se tuvieron a la hora de desarrollar la API.

# Módulo meli

## Optimización de los recursos del sistema operativo
Se construyendo las clases que derivan de ApiMeli con la principal preocupación de que no hubiera tiempos muertos de espera entre llamada a la API en la nube y la persistencia de los datos en la DB. Mientras un determinado "objeto" se encuentra a la espera de la información que provee su API asignada, otro objeto deberá aprovechar este tiempo para seguir procesando, consumiendo y persistiendo los datos.\
Para este fin se usaron las corrutinas y las funciones asincrónicas, para evitar la espera.\
Como futura mejora se puede analizar el hecho de aprovechar los múltiples CPUs del sistema, ni hablar usar recursos servidores virtualres en paralelo para distribuir el procesamiento.\

Se ensayaron diferentes cantidades de tareas concurrentes, desde un valor muy bajo como "8" workers a "2000", el resultado que se obtuvo de esa experencia fue el siguiente:\
Tiempo requerido para consumir el archivo de 200 items con diferentes cantidades de tareas concurrentes:\
![Inove banner](/images/tiempo_ejecucion.png)

## Flexibilidad a la hora de encadenar más API call
Se propuso que el sistema fuera flexible a la hora de sumar más APIs a la cadena. Para esto se desarrollo una clase base __ApiMeli__ de la cual deberiban las clases de __ItemApi__, __CategoryApi__ y __CurrencyApi__ (faltó la de UserApi por un problema menor, pero la implementación es exactamente igual).\
En el constructor de cualquiera de la APIs mencionadas se puede pasar como parámetro la lista de API call que dicha API deberá realizar durante su proceso de carga.\
El proceso de carga "__load__" realiza el consumo de la API "__featch__" y de todas sus APIs encadenadas a esta, es un proceso en cadena el cual pueden a su vez encadenarse más eslabones en cualquier parte de la cadena.\
Este proceso es flexible y fácil de escalar gracias a los siguientes patrones de diseño:

#### Factory
Las APIs que se encadenan al la "API principal" se realiza de forma muy fexible mediante el archivo de configuración gracias al pattern de __Factory__, el cual permite instanciar un objeto por su nombre de clase. Por un tema de tiempos se implementó el pattern de __Factory__ utilizando un diccionario, lo cual requiere el completado a mano del mismo cuando se agrega una clase derivada de ApiMeli.\
Como propuesta futura se implementará el pattern al 100% para automatizar el registro de las clases, por un tema de tiempo se optó por la funcionalidad inmedianta.

#### Decorator
¿Cómo es que las APIs que se lanzan en cadena a la principal agregan las funcionalidades dinámicamente al objeto que las lanzó? Para esto se utiliza el pattern de __Decorator__\.
Llamaremos objeto "principal" al que posee la lista de APIs call a realizar en cadena (lista de objetos ApiMeli para ejecutar fetch), y objeto "secundario" a aquel que fue lanzado por el "principal" en cadena a su proceso de carga.\
Este pattern permite que el objeto "principal" sea pasado como referencia al objeto secundario que continue la información de valor agregado. Este objeto sabe como "__decorar__" al objeto principal por lo que pasa los valores de interés a este.\
Es un proceso sumamente flexible porque la clase del objeto "secundario" es la que tiene le conocimiento de sus datos y por ende de los datos que le pueden servir de utilidad al objeto pasado por parámetro, por lo que lo decora con la información que posee.


#### Persistencia distribuida
El problema en cuestión solicitaba que el objeto "item" recolectara toda la información y realizara la persistencia en una única tabla de la DB. Aún así el sistema se lo preparó para que cada clase derivada de __ApiMeli__ pudiera persistir los datos en la DB de forma asincrónica en la tabla que see. Cada clase podría completar una tabla distinta.

# Módulo stream

## Optimización de los recursos del sistema operativo
Se desarrollaron diferentes clases de consumo de datos (stream) de diferentes tipos:
- CSV --> CsvStream
- Txt --> TxtStream
- Jsonline --> JsonlStream

La premisa más importante fue no consumir todos los recursos del sistema operativo en el caso de que el stream a consumir fuera más grande que la propia memoria del sistema. Para eso se implementó el mecanismo de "__chunks__".\
El proceso consta de leer al archivo "trozos" en función de los recursos y la cantidad de tareas concurrentes. El objetivo final si se lo deseara sería poder paralelizar dichos __chunks__ en CPUs o procesos virtual distribuidos.

## Flexibilidad a la hora de sumar otro método de stream
Tal como se mencionó antes, en el caso del módulo de stream tambíen se utilizó el concepto de __Factory__ para instanciar dinámicamente el tipo de stream deseado según la configuración del sistema.\
Además, se separo la responsabilidad de consumo de archivo y producción de "chunks" del mecanismo de "parse" y "preparación" de los datos para su consumo.\
Se puede aprovechar el método "__parse_line__" de cualquiera de las clases sin necesidad de abrir el archivo en cuestión, por lo que puede aprovecharse en un endpoint del tipo POST para ingresar datos a la DB.

# unit test
Se generaron algunos unit test tanto del módulo de "__meli__" como el de "__stream__", no contemplan todos los casos posibles pero fueron útiles para las primeras pruebas con las APIs.

# Flask server
La API la lanza "server.py" que llama al archivo app.py en donde se encuentran todos los handlers de los endpoints implementados. Se dividio el repositorio en directorios para no acomplar las responsabilidades, aún puede trabajarse en ese punto (por ejemplo, colocar los handlers en un archivo separado).

# Dificultades durante el diseño

## Diseño
La mayor parte del esfuerzo se colocó en que el sistema fuera lo más óptimo posible en cuando a los tiempos de consumo y tiempos muertos, en prepararlo para escalar y modificar de la forma más amigable posible.\
Otra cosas fueron planteadas y capaz no completadas como:
- El pattern de Factory quedó a medio hacer, falta implementarlo adecuadamente para poder registrar las clases.
- En principio no fue simple resolver lo de TOKEN_ACCESS para pegarle a la API de Users para obtener el nickname del seller_id, como su implementación con los decorator y la Factory era un 99% igual a cualquiera de las otras la deje de lado para futura revisión.
- Aún hay tela para cortar para hacer más óptimo el sistema, no se está aprovechando los multi Cores del sistema en sí, pero por lo que entiendo lo práctico es usar single CPU y single thread pero en múltiples sistemas distribuidos.

## Postgres
postgreSQL requirió más tiempo de lo estimado en comparación a otras veces, por momentos la base quedaba como si hubiera faltado cerrar una transacción y no era posible ni borrar la base ni la tabla, pero sí agregar filas a ella. Un comportamiento raro que antes no me había pasado con postgres.\
Hasta ahora siempre había usado sqlalchemy, pero como en definitiva termino siempre haciendo querys "crudas" para estos casos simples no valia la pena cargar al sistema con tanto cuando psycopg alcanza y sobra para el uso dado. Capaz hay algo con psycopg que se me escapa y por eso surgieron los problemas.
