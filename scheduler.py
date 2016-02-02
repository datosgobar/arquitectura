
import json
import subprocess
import datetime

from celery import Celery
from celery.exceptions import Ignore
from scheduler_db_mgmt import ETLRun, ETLModuleRun
import scheduler_db_mgmt

app = Celery('task', backend='amqp', broker='amqp://guest@localhost//')

etl_sequences_dir = "./etl_sequences/"
modules_file = "./modules.json"


@app.task
def error_handler(uuid):
    print "error", uuid


@app.task
def start_etl(etl_run_name) : 
    sess = scheduler_db_mgmt.get_session()
    etl_run = ETLRun(name=etl_run_name, start=datetime.datetime.now())
    sess.add(etl_run)
    sess.commit()
    
    etl_sequence_path = "%s/%s.json" % (etl_sequences_dir, etl_run_name)
    
    
    etl_sequence = json.load(open(etl_sequence_path))
    for i in range(len(etl_sequence)) :
        etl_module_run = ETLModuleRun(
            name=etl_sequence[i]["module_name"],
            input=etl_sequence[i]["input"],
            output=etl_sequence[i]["output"],
            conf=etl_sequence[i]["conf"],
            status="NEW",
            etl_run_id=etl_run.id
        )
        sess.add(etl_module_run)
        sess.commit()
        etl_sequence[i]["etl_module_run_id"] = etl_module_run.id
    
    sess.close()
    
    taskchain = reduce(lambda c,p: c | p, [exec_module.si(**p) for p in etl_sequence])
    taskchain = taskchain | end_etl.si(etl_run_id=etl_run.id)
    taskchain()


@app.task
def end_etl(etl_run_id) :
    sess = scheduler_db_mgmt.get_session()
    etl_run = sess.query(ETLRun).get(etl_run_id)
    etl_run.end = datetime.datetime.now() 
    sess.add(etl_run)
    sess.commit()
    sess.close()


@app.task(bind=True)
def exec_module(self, etl_module_run_id=None, module_name=None, input=None, output=None, conf=None, task_id=None):
    print (module_name, input, output, conf, task_id)
    
    sess = scheduler_db_mgmt.get_session()
    etl_module_run = sess.query(ETLModuleRun).get(etl_module_run_id)
    etl_module_run.start = datetime.datetime.now() 
    etl_module_run.status = "STARTED"
    sess.add(etl_module_run)
    sess.commit()
    sess.close()

    
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
    
    sess = scheduler_db_mgmt.get_session()
    etl_module_run = sess.query(ETLModuleRun).get(etl_module_run_id)
    etl_module_run.end = datetime.datetime.now() 
    
    if exit_code == 0 :
        print "Sucess!"
        self.update_state(state='SUCCESS')
        etl_module_run.status = 'SUCCESS'
    else :
        print "Fail!"
        self.update_state(state='FAILURE')
        self.request.callbacks = [error_handler]
        etl_module_run.status = 'FAILURE'
    
    sess.add(etl_module_run)
    sess.commit()
    sess.close()
    
    return exit_code

