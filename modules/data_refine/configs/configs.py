"""configuraciones para el modulo de refine."""

# Configuraciones para el servidor de OpenRefine.
refine_server_config = {
    'executable_path': '/direccion/a/el/ejecuutable/de/OpenRefine_server',
    'host': 'localhost',
    'port': '3333',
    'protocol': 'http',
    'allawed_urls': '0.0.0.0'
}

cmd_line_args = ['input', 'output']
inputs_names = ['data00', 'data01', 'data02']
inputs_format = 'csv'
filters_name = 'filter_'
filters_folder = 'filters'
filters_format = 'json'
