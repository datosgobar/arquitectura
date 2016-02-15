#!/usr/bin/env python

import json
import os
from os import path
import sys
from configs import configs
from libs import refine
import urllib2
import subprocess
import time

import module_base

class DataRefineModule(module_base.ModuleBase) :
    prog_text   = "main.py"
    desc_text = "Process input files with the given filters using OpenRefine"
    input_text = "Directory where the input CSVs are stored"
    output_text = "Directory where the output files will be stored"
    conf_text = "Configuration parameters"
    epilog = """
    """
    input_required = True
    output_required = True
    conf_required = True


    def refine_server_is_reachable(self, server_url, check_cout=1):
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


    def start_refine_server(self, server_settings, server_url):
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
        return self.refine_server_is_reachable(server_url, 2)


    def load_inputs(self, inputs_folder, conf, filters_folder):
        """
        funcion que carga y chequea la existencia de las inputs requeridas.

        :type inputs_folder: Str
        :param inputs_folder: String provisto por cmd-line args, especifica donde
                              se encuentran las inputs requeridas.
        :returns :type Bool:
        """
        app_main_folder = path.dirname(path.abspath(__file__))
        response = []
        for r_input in os.listdir(inputs_folder):
            i_name = os.path.join(inputs_folder, r_input)
            r_input = r_input.split(".")[0]
            ref_filter = '{prefix}{name}.{format}'.format(
                    prefix=conf["filters_name"],
                    name=r_input,
                    format=conf["filters_format"])
            ref_filter = path.join(filters_folder, ref_filter)
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
    
    def push_data_into_refine(self, files_to_refine, output_folder, conf):
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
                if not self.refine_server_is_reachable(open_refine_server):
                    if not self.start_refine_server(
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
                outfile = '{name}_refined.{format}'.format(
                                                    name=file_to_refine['name'],
                                                    format=conf["outputs_format"])
                refined_data = path.join(output_folder, outfile)
                with open(refined_data, 'w') as data:
                    data.write(p.export_rows().replace('\t', ';'))
                p.delete_project()
            except Exception, e:
                print 'ERROR: Fallo export de datos filtrados por OpenRefine'\
                      '\n{Exception_msg}'.format(Exception_msg=e)
                return False
        return True
    
    def implementation(self, input=None, output=None, conf=None) :
        conf_data = json.load(open(path.join(conf, "conf.json")))
        filters_folder = path.join(conf, "filters")
        files_dict = self.load_inputs(input, conf_data, filters_folder)
        print files_dict
        if not files_dict:
            print 'error, fallo carga de inputs requeridas'
            exit(1)
        if not self.push_data_into_refine(files_dict, output, conf_data):
            print 'Fallo Limpieza de datos...'
            exit(1)
        print 'Flawless victory!'

if __name__ == '__main__':
    module = DataRefineModule()
    module.run()
