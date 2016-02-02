
import json
import subprocess

from celery import Celery
from celery.exceptions import Ignore

app = Celery('task', backend='amqp', broker='amqp://guest@localhost//')

etl_sequences_dir = "./etl_sequences/"
modules_file = "./modules.json"

@app.task
def error_handler(uuid):
    print "error", uuid

@app.task
def start_etl(etl_run_name) : 
    etl_sequence_path = "%s/%s.json" % (etl_sequences_dir, etl_run_name)
    print etl_sequence_path
    etl_sequence = json.load(open(etl_sequence_path))
    
    taskchain = None
    for p in etl_sequence :
        if not taskchain :
            taskchain = exec_module.si(**p)
        else :
            taskchain = (taskchain | exec_module.si(**p))
    
    taskchain()
    

@app.task(bind=True)
def exec_module(self, module_name=None, input=None, output=None, conf=None, task_id=None):
    print (module_name, input, output, conf, task_id)
    modules = json.load(open(modules_file))
    module_cmd = modules[module_name]["cmd"]
    
    module_params = []
    if input :
        module_params += ["--input", input]
    if output :
        module_params += ["--output", output]
    if conf :
        module_params += ["--conf", conf]
        
    exit_code = subprocess.call([module_cmd]+module_params)
    if exit_code == 0 :
        print "Sucess!"
        self.update_state(state='SUCCESS')
    else :
        print "Fail!"
        self.update_state(state='FAILURE')
        self.request.callbacks = [error_handler]
    
    #module_finished(task_id)
    
    return exit_code

