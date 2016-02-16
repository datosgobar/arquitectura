
import json
import subprocess
import datetime
import time
import os

from celery import Celery
from celery.exceptions import Ignore
from scheduler_db_mgmt import ETLRun, ETLModuleRun
import scheduler_db_mgmt

app = Celery('task', backend='amqp', broker='amqp://guest@localhost//')

etl_sequences_dir = "./etl_sequences/"
modules_file = "./modules.json"

debug_slowdown = 0.35
#debug_slowdown = None

@app.task
def error_handler(failed_etl_module_run_id):
    sess = scheduler_db_mgmt.get_session()
    etl_module_run = sess.query(ETLModuleRun).get(failed_etl_module_run_id)
    etl_run = sess.query(ETLRun).get(etl_module_run.etl_run_id)
    etl_run.status = "FAILURE"
    etl_run.end = datetime.datetime.now()
    sess.add(etl_run)
    sess.commit()
    sess.close()


@app.task
def start_etl(etl_run_name) : 
    sess = scheduler_db_mgmt.get_session()
    etl_run = ETLRun(name=etl_run_name, start=datetime.datetime.now(), status="PENDING")
    sess.add(etl_run)
    sess.commit()
    
    etl_sequence_path = "%s/%s.json" % (etl_sequences_dir, etl_run_name)
    
    etl_sequence = json.load(open(etl_sequence_path))
    for i in range(len(etl_sequence)) :
        etl_module_run = ETLModuleRun(
            name=etl_sequence[i]["module_name"],
            input=etl_sequence[i].get("input", None),
            output=etl_sequence[i].get("output", None),
            conf=etl_sequence[i].get("conf", None),
            status="PENDING",
            etl_run_id=etl_run.id
        )
        sess.add(etl_module_run)
        sess.commit()
        etl_sequence[i]["etl_module_run_id"] = etl_module_run.id
    
    
    taskchain = reduce(lambda c,p: c | p, [exec_module.si(**p) for p in etl_sequence])
    taskchain = taskchain | end_etl.si(etl_run_id=etl_run.id)
    sess.close()
    
    taskchain()


@app.task
def end_etl(etl_run_id) :
    sess = scheduler_db_mgmt.get_session()
    etl_run = sess.query(ETLRun).get(etl_run_id)
    etl_run.end = datetime.datetime.now() 
    etl_run.status = "SUCCESS"
    sess.add(etl_run)
    sess.commit()
    sess.close()


@app.task(bind=True)
def exec_module(self, etl_module_run_id=None, module_name=None, input=None, output=None, conf=None, task_id=None):
    if debug_slowdown :
        time.sleep(debug_slowdown)

    print (module_name, input, output, conf, task_id)
    
    sess = scheduler_db_mgmt.get_session()
    etl_module_run = sess.query(ETLModuleRun).get(etl_module_run_id)
    #etl_module_run.task_id = exec_module.request.id
    etl_module_run.task_id = task_id
    etl_module_run.start = datetime.datetime.now() 
    etl_module_run.status = "STARTED"
    sess.add(etl_module_run)
    sess.commit()
    sess.close()
    
    modules = json.load(open(modules_file))
    module_cmd = modules[module_name]["cmd"]
    if not os.path.isabs(module_cmd) :
        module_cmd = os.path.abspath(os.path.join(os.path.dirname(modules_file), module_cmd))
    
    module_params = []
    if input :
        module_params += ["--input", input]
    if output :
        module_params += ["--output", output]
    if conf :
        module_params += ["--conf", conf]
        
    if debug_slowdown :
        time.sleep(debug_slowdown)

    exit_code = subprocess.call([module_cmd]+module_params)
    
    #proc = subprocess.Popen([module_cmd]+module_params)
    #print proc.communicate()
    #exit_code = proc.wait()
    #data = sp.Popen(openRTSP + opts.split(), stdout=sp.PIPE).communicate()[0]
    #data = subprocess.Popen([module_cmd]+module_params, stdout=subprocess.PIPE).communicate()[0]
    
    #proc = subprocess.Popen([module_cmd]+module_params, stdout=subprocess.PIPE)
    #print [module_cmd]+module_params
    #output = proc.communicate()[0]
    #exit_code = proc.returncode 
    #print output
    #print data, exit_code
    
    if debug_slowdown :
        time.sleep(debug_slowdown)
    
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
        etl_module_run.status = 'FAILURE'
        self.request.callbacks = [error_handler]
    
    etl_module_run_id = etl_module_run.id
    sess.add(etl_module_run)
    sess.commit()
    sess.close()
    
    if debug_slowdown :
        time.sleep(debug_slowdown)
    
    return etl_module_run_id

