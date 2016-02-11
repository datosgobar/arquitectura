
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
      'executable_path': '/direccion/a/el/ejecuutable/de/OpenRefine_server',
      'host': 'localhost',
      'port': '3333',
      'protocol': 'http',
      'allawed_urls': '0.0.0.0'
  }
  ```
  *Mas info en repo de [OpenRefine](https://github.com/OpenRefine/OpenRefine)*

* Configurar argumentos requeridos por el modulo:

  *refine_module/configs/configs.py* [12,0]

  ```Python
  cmd_line_args = ['input', 'output']
  ```

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
