u"""Modulo de de refinamiento de dados.

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
"""

from os import path
import sys
from configs import configs
from libs import refine
import urllib2
import subprocess
import time


def refine_server_is_recheable(server_url, check_cout=1):
    """Funcion que chequea que que pueda acceder al servidor de OpenRefine.

    :type server_url: Str
    :param server_url: protocolo, host y puerto donde se encuentra el
    servidor de refine
    """
    try:
        urllib2.urlopen(server_url, timeout=2)
        print 'is ok'
    except urllib2.URLError:
        print 'El servidor no es accesible, intento: %d' % check_cout
        return False
    return True


def start_refine_server(server_settings, server_url):
    """funcion que intenta iniciar el servidor de OpenRefine.

    :param: server_url:
        :type server_settings: Dict
    :param: server_url:
        :type server_url: Str
    :returns
        * :type Bool.
        * True si logro iniciar correctamente el server,
        False si ocurrio un problema.
    """
    if not path.exists(server_settings['executable_path']):
        print 'Error: la direcccion provista al ejecutable de '\
              'OpenRefine no existe'
        return False
    cmd = '{or_exec_path}/refine -i {or_allawed_urls} -p {or_port}&'.format(
        or_exec_path=server_settings['executable_path'],
        or_allawed_urls=server_settings['allawed_urls'],
        or_port=server_settings['port'])
    try:
        subprocess.Popen(cmd, shell=True)
    except OSError:
        print 'Error al ejecutar comando'

    # Espero 10 segundos hasta que termine de iniciar el server de openRefine,
    # para chequear q verdaderamente este en funcionamiento
    time.sleep(10)
    return refine_server_is_recheable(server_url, 2)


def load_inputs(inputs_folder):
    """
    funcion que carga y chequea la existencia de las inputs requeridas.

    :type inputs_folder: Str
    :param inputs_folder: String provisto por cmd-line args, especifica donde
                          se encuentran las inputs requeridas.
    :returns :type Bool:
    """
    app_main_folder = path.dirname(path.abspath(__file__))
    filters_folder = path.join(app_main_folder, configs.filters_folder)
    required_inputs = configs.inputs_names
    required_inputs_format = configs.inputs_format
    response = []
    for r_input in required_inputs:
        i_name = '{name}.{format}'.format(name=r_input,
                                          format=required_inputs_format)
        ref_filter = '{prefix}{name}.{format}'.format(
                name=r_input,
                format=configs.filters_format,
                prefix=configs.filters_name)
        ref_filter = path.join(filters_folder, ref_filter)
        i_name = path.join(inputs_folder, i_name)
        if path.exists(i_name) and path.exists(ref_filter):
            e = {
                'name': r_input,
                'file': i_name,
                'filter': ref_filter
            }
            response.append(e)
        else:
            print 'Error, Archivo requerido no existe'
            return False
    return response


def push_data_into_refine(files_to_refine, output_folder):
    """
    Docstring para que no joda pep8.

    :type output_folder: Str.
    :param output_folder: provisto por cmd-line args, especifica donde se
                          depositara la salida del modulo.
    :param files_to_refine:
    """
    open_refine_server = '{protocol}://{host}:{port}'.format(
            host=configs.refine_server_config['host'].lower(),
            port=configs.refine_server_config['port'],
            protocol=configs.refine_server_config['protocol'].lower())
    for file_to_refine in files_to_refine:
        try:
            if not refine_server_is_recheable(open_refine_server):
                if not start_refine_server(
                        configs.refine_server_config,
                        open_refine_server):
                    return False
            r = refine.Refine(server=open_refine_server)
            p = r.new_project(file_to_refine['file'])
            p.apply_operations(file_to_refine['filter'])
        except Exception, e:
            print e
            return False
        try:
            data_export = '{name}_refined.{format}'.format(
                                                name=file_to_refine['name'],
                                                format=configs.inputs_format)
            refined_data = path.join(output_folder, data_export)
            with open(refined_data, 'w') as data:
                data.write(p.export_rows().replace('\t', ';'))
            p.delete_project()
        except Exception, e:
            print 'ERROR: Fallo export de datos filtrados por OpenRefine'\
                  '\n{Exception_msg}'.format(Exception_msg=e)
            return False
    return True


def load_cmd_line_args():
    """
    Funcion basica que carga y valida los argumentos recibidos x cmd-line.

    :returns
        :type: Bool
        True si puede encontrar y validar la existencia de todos los campos
        requeridos en la configuracion del modulo.
    """
    cmd_args = sys.argv
    r = {}
    if len(cmd_args) > len(configs.cmd_line_args) * 2:
        for arg in configs.cmd_line_args:
            sa = '--{arg}'.format(arg=arg)
            if sa in cmd_args:
                try:
                    r[arg] = cmd_args[cmd_args.index(sa) + 1]
                except IndexError:
                    print 'Error: Argumentos mal formado'
                    exit(1)
                except Exception, e:
                    print e
                    print 'Error: fallo carga de cmd-line args'
                    exit(1)
        return r
    else:
        print 'Error, Argumentos x cmd line, insuficientes'
        exit(1)


def main():
    """Docstring para que no joda pep8."""
    io_dict = load_cmd_line_args()
    files_dict = load_inputs(io_dict['input'])
    if not files_dict:
        print 'error, fallo carga de inputs requeridas'
        exit(1)
    if not push_data_into_refine(files_dict, io_dict['output']):
        print 'Fallo Limpieza de datos...'
        exit(1)
    print 'Flawless victory!'


if __name__ == '__main__':
    main()
