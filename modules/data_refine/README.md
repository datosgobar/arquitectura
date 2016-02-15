
# Modulo simple OpenRefine
### Contenido del Modulo:
    refine_module
        |
        `---main.py #main del Modulo
        |
        `---requirements.txt
        |
        `---configs
        |       |
        |       `---__init__.py
        |       |
        |       `---configs.py #Configuraciones del Modulo
        |
        `---libs
        |     |
        |     `---refine.py #Lib de OpenRefine
        |     |
        |     `---__init__.py
        |
        `---filters
                |
                `---filtro_01.json filtros utilizados con OpenRefine
                        ...
### Instalacion:
    sudo pip install -r requirements.txt

### Preconfiguracion:

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

### Configuracion de Ejecucion:
Las configuraciones de cada corrida particular se definien mediante un directorio indicado por el parametro `--config`
Este directorio debe contener un archivo `config.json` el cual indica parametros generales de ejecucio y un directorio `filters` donde se especifican los filtros de OpenRefine que se van a aplicar a cada archivo de entrada.

Ejemplo de `config.json`:
```
{
    "inputs_format" : "csv",
    "filters_name" : "",
    "filters_format" : "json"
}
```

Donde:
- inputs_format
- filters_name: Sufijo utilizando para identificar los nombres de los filtros a aplicar
- filters_format : "json"


* Configurar nombres de las inputs esperadas por el modulo:

    *refine_module/configs/configs.py* [13,0]

    ```Python
    inputs_names = ['data00', 'data01', 'data02']
    ```

* Configurar formato de las inputs esperadas por el modulo:

    *refine_module/configs/configs.py* [14,0]

    ```Python
    inputs_format = 'csv'
    ```

* Configurar filtros:

    *refine_module/configs/configs.py* [15,0]

    ```Python
    filters_name = 'filter_'
  filters_folder = 'filters'
  filters_format = 'json'
    ```


### Ejecución:

Archivo principal del modulo es "main.py"

    ./main.py --input carpeta/de/entrada --output carpeta/de/salida
