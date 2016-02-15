
# Modulo simple para filtrado por OpenRefine
# Contenido del Modulo:
    refine_module
        |
        `---data_refine.py #main del Modulo
        |
        `---requirements.txt
        |
        `---configs
        |       |
        |       `---__init__.py
        |       |
        |       `---configs.py # Configuraciones del Modulo
        |
        `---libs
        |     |
        |     `---refine.py # Lib de OpenRefine
        |     |
        |     `---__init__.py
        |
        `---sample  # Directorio con datos de ejemplo
                |
                `---input # Directorio de entrada de ejemplo
                |     |
                |     `---Contrataciones.csv # Entrada de ejemplo
                |
                `---output # Directorio de salida de ejemplo
                |     |
                |     `---Contrataciones_refined_test.csv # Salida esperada de la ejecucion de ejemplo
                |
                `---conf # Directorio de configuracion de ejemplo
                        |
                        `---conf.json # Archivo de configuracion
                        |
                        `---filters # Directorio con filtros
                              |
                              `---Contrataciones.json # Filtro que se aplica a Contrataciones.csv

# Instalacion:
    sudo pip install -r requirements.txt

# Preconfiguracion:

* Configurar parametro para servidor de OpenRefine en:

  *refine_module/configs/configs.py* [4,0]

  ```Python
  refine_server_config = {
      'executable_path': '/direccion/a/el/ejecutable/de/OpenRefine_server',
      'host': 'localhost',
      'port': '3333',
      'protocol': 'http',
      'allawed_urls': '0.0.0.0'
  }
  ```
  *Mas info en repo de [OpenRefine](https://github.com/OpenRefine/OpenRefine)*

# Configuracion de Ejecuciones:
Las configuraciones de cada corrida particular se definien mediante un directorio indicado por el parametro `--config`
Este directorio debe contener un archivo `config.json` el cual indica parametros generales de ejecucio y un directorio `filters` donde se especifican los filtros de OpenRefine que se van a aplicar a cada archivo de entrada.

Ejemplo de `config.json`:
```
{
    "inputs_format" : "csv",
    "outputs_format" : "csv",
    "outputs_suffix" : "_refined",
    "filters_name" : "",
    "filters_format" : "json"
}
```

Donde:
- inputs_format: Formato de los archivos de entrada. (Eg: csv)
- outputs_format: Formato de los archivos de entrada. (Eg: csv)
- outputs_suffix: Sufijo prependeado a los archivos de salida. (Eg: _refined)
- filters_name: Prefijo utilizando para identificar a qlos nombres de los filtros a aplicar
- filters_format : "json"

# Ejecución:

Archivo principal del modulo es "data_refine.py".
El siguiente comando realiza una transformacion siguiendo las configuraciones de ejemplo
```
    ./data_refine.py --input ./sample/input/ --output ./sample/output/ --conf ./sample/conf/
```
