
# Modulo para carga de CSVs en Bases de Datos
## Contenido del Modulo:
    db_loader
        |
        `---db_loader.py # Main del Modulo
        |
        `---module_base.py # Clase wraper de base
        |
        `---requirements.txt
        |
        `---sample_conf.json # Archivo de configuracion de ejemplo

## Instalacion:
    sudo pip install -r requirements.txt

## Parametros:

- `--input`: Directorio con CSVs desde donde se van a cargar los datos
- `--output`: Connection string de la DB donde se quieren cargar los datos
- `--conf`: JSON de configuracion del proceso

## Formato de entrada
El directorio identificado por ```--input``` debe contener archivos que comiencen por le nombre de la tabla objetivo separada por punto y que terminen en ```.csv```.

## Configuracion de ejemplo:
Los parametros para la carga de los datos en la DB se especifican mediante el archivo de configuracion especificado por el argumento ```--conf```. Para ver un ejemplo de esto consultar ```sample_conf.json```

Dicho archivo tiene la estructura:
```
{
    "create_all" : true,
    "clear_all_tables_before_insert" : true,
    "add_pk" : true,
    "delimiter" : ",",
    "table_desc" : [{
        "name" : "iris",
        "columns" : [
            {
                "name" : "sepal_length",
                "type" : "Float"
            }
        ]
    }]
}
```

Donde:
- create_all: Crear todas las tablas
- clear_all_tables_before_insert" : Dropea todas las tablas antes de cargarlas
- add_pk: Crea una primary key `id` para la nueva tabla
- delimiter: Caracter de separacion entre campos
- table_desc: Descripcion de la tabla
-- name: Nombre de la tabla donde se van a cargar los datos. El nombre del archivo input debe comenzar con el nombre de la tabla objetivo.
-- columns: Especificacion de las columnas de la tabla
--- name: Nombre de la columna. Debe existir en el archivo de entrada.
--- type: Tipo de la columna. Puede ser uno de los siguiente: String, Text, Integer, BigInteger, Float, Boolean, Date, Time o DateTime.

## Ejecución:
Archivo principal del modulo es "main.py".
Si se ejecuta de la siguiente manera se deberia crear una base de datos SQLite en `sample/output.sqlite` con los datos extraidos de `sample/input/iris.csv`.
```
    ./db_loader.py --input sample/input/ \
                          --output "sqlite:///.//sample/output.sqlite" \
                          --conf sample/conf.json

```