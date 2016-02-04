
from flask import Flask, jsonify
import json

import scheduler_db_mgmt
from scheduler_db_mgmt import ETLRun, ETLModuleRun

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/getstatus')
def getstatus():
    sess = scheduler_db_mgmt.get_session()

    ret = []
    for er in sess.query(ETLRun).all() :
        etlrun_data = { a: str(getattr(er, a)) for a in ["id", "name", "start", "end", "status"]}
        etlmodulerun_data = []
        for emr in sess.query(ETLModuleRun).filter(ETLModuleRun.etl_run_id==er.id).all() :
            etlmodulerun_data += [{ a: str(getattr(emr, a)) for a in ["id", "task_id", "name", "input", "output", "conf", "start", "end", "status"]}]
        
        etlrun_data["modules"] = etlmodulerun_data
        ret += [etlrun_data]
    sess.close()
    #print json.dumps(ret, indent=4)
    return json.dumps(ret)

@app.route('/')
def index():
    data = open("scheduler.html").read()
    return data

if __name__ == '__main__':
    app.run(debug=True)

