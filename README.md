
# Arquitectura
Dada la gran cantidad de datasets con los que trabaja esta oficina resulta necesario definir una arquitectura para automatizar el manejo de los mismos y que ademas facilite su explotacion.

## ETL
La primera etapa de este proceso consiste de las tareas necesarias para extraer datos de sus fuentes originales, transformarlos a un formato normalizado y finalmente cargarlos en una base de datos centralizada. 

### Scheduler
Para automatizar estos procesos se considero apropiado implementar un scheduler que ejecuta secuencias de modulos utilizando una interfaz estandarizada. La manera en la que se definen tanto las secuencias como los modulos se explica en las secciones subsiguientes

Este proceso esta implementado mediante una serie de tareas de Celery que interactuan mediante una cola de mensajes.
Este sistema tambien dispone de una base de datos para hacer el seguimiento de los procesos de ETL como un todo como asi tambien de la ejecucion de los modulos particulares que lo componen.

En el siguiente diagrama de flujo muestra como se suceden las tareas que conforman una secuencia cualquiera de ETL:
```
                                                       error_handler
                                                            ^                    
Un cron o comando externo                                   |                    
inicial el proceso indicando    ---> start_etl -------> exec_module --...---> end_etl
la secuencia ETL para ejecutar            ^                 ^
                                          |                 |
                                   elt_sequences/      modules.json
```

1. El proceso inicia cuando se llama a la tarea start_etl a la cual se le pasa como argumento el nombre de la secuencia que se quiere ejecutar, llamemosla dummy_etl.
2. La tarea start_etl busca el archivo dummy_etl.json en el directorio etl_sequences/, deja configurada la secuencia de modulos correspondiente y la inicia. Con esto se deja indicado que la tareas exec_module sera llamada en el momento que resulte apropiado pasandole una serie de parametros que se describiran mas adelante.
3. Cuando se ejecuta un modulo se accede al archivo modules.json para determina que comando ejecutar. Este comando se ejecutar junto con los parametros especificados para esa secuencia.
4. Una vez que el comando termina pueden ocurrir dos cosas:
5. Si el comando termino de manera correcta se procede a llamar al modulo que le sigue en la secuencia si corresponde o bien a la tarea end_etl en la cual se marca al proceso de ETL como exitoso. Caso contrario se llama a la tarea error_handler luego de los cual termina el proceso y se marca ese proceso de ETL como fallido.


### Definicion de secuencias ETL
Las secuencias de modulos necesarios para llevar a cabo el proceso de ETL se definen mendiante un archivo json situado en la carpeta elt_sequences/.
Dicho archivo podria tener una estructura como la siguiente:
dummy_etl.json
```
[
    {
        "module_name" : "dummy_extractor",
        "input" : "",
        "output" : "/var/etl/dummy_raw.csv",
        "conf" : ""
    },
    {
        "module_name" : "dummy_transformer",
        "input" : "/var/etl/dummy_raw.csv",
        "output" : "/var/etl/dummy_clean.csv",
        "conf" : "transformer_config.json"
    },
    {
        "module_name" : "dummy_loader",
        "input" : "/var/etl/dummy_clean.csv",
        "output" : "",
        "conf" : ""
    }
]
```

### Modulos
Los modulos tienen la funcion de ejecutar tareas particulares de ETL, como podria ser extraer datos de una pagina web, pasar el input por OpenRefine o cargarlos en una base de datos.

##### Interfaz de los modulos 
Para facilitar el manejo de los modulos se definio que tengan una interfaz unificada y que reporten si su ejecucion fue exitosa mediante el errorcode. 0 es que no hubo error y 1 uno es que algo fallo y hay que interrupir el proceso de ETL.
```
COMMAND [--input PATH] [--output PATH] [--config PATH]
```

Los argumentos que puede admitir un comando que implemente esta interfaz son los siguientes:
--input : Ruta de algun tipo que indica el origen de los datos que se quiere procesar
--output : Ruta de algun tipo que indica el destino de los datos ya procesador
--config : Otros parametros de ejecucion del modulo

Es importante tener en cuenta que estos parametros son opcionales. Por ejemplo un modulo de extraccion de datos podria conocer de antemano la fuente de los datos que va a cargar (este seria el caso de un scraper por ejemplo).
La funcion del argumento config es la de brindar una forma de pasar informacion extra al modulo. Un ejemplo de esto seria indicarle a un modulo de OpenRefine que tipo de transformaciones se quieren ejecutar.

Siguiendo los ejemplos anteriores de al ejecutar el primer modulo de dummy_etl.json se generaria un comando como el siguiente:
```
./dummy_transformer.sh --input "/var/etl/dummy_raw.csv" --output "/var/etl/dummy_clean.csv" --conf "transformer_config.json"
```

#### Definicion de modulos
El archivo modules.json indica el mapeo entre el campo module_name en el archivo json de secuencias ETL y el comando que se debe ejecutar:
Eg:
```
{
    "dummy_extractor" : {
        "cmd" : "./dummy_extractor.sh"
    },
    "dummy_transformer" : {
        "cmd" : "./dummy_transformer.sh"
    },
    "dummy_loader" : {
        "cmd" : "./dummy_loader.sh"
    }
}
```

#### Module wrapper
El wrapper tiene el proposito de generar un entorno para correr las tareas de manera sencilla.
[TODO]

### Instrucciones
#### Como iniciar el sistema
Iniciar las tareas del scheduler:
```
celery -A scheduler worker -l info
```

Iniciar ui de monitoreo del scheduler:
```
python scheduler_ui.py
```

#### Como iniciar secuencias de ETL
Para iniciar la tarea de ETL llamada 'test' tendria que ejecutar este comando:
```
$ python -c "from scheduler import start_etl; start_etl.delay(etl_run_name='test')"
```


