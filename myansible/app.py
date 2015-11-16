#!/usr/bin/python
from flask import Flask, jsonify, url_for
from celery import Celery
import time

import json
import pymongo
from bson import json_util

connection = pymongo.MongoClient()
db = connection.ansible
inv = db.inventory

import ansible.playbook
from ansible import callbacks
from ansible import utils
import ansible.inventory

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'top-secret!'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/run/', methods=['GET', 'POST'])
def run():
    run = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('get_results',job_id=run.id)}

@app.route('/run/results/<job_id>', methods=['GET'])
def get_results(job_id):
    job = long_task.AsyncResult(job_id)
    print job.__dict__
    if job.state == 'PENDING':
        response = {
	    'state': job.state,
	    'status': 'Pending'
	}
    elif job.state == 'STARTED':
	responese = {
	    'state': job.state, 
	    'status': "Started"
	}
    elif job.state == 'FAILURE':
	response = {
	    'state': job.state,
	    'status': job.info
	}
    elif job.state == 'SUCCESS':
	response = {
	    'state': job.state,
	    'status': job.info
	}
        #if 'result' in job.info:
	    #response['result'] = job.info['result'] 
    else:
        response = {
            'state': job.state,
            'status': job.info
        }
    return jsonify(response)

@celery.task()
def long_task():
    return get_playbook().run()

def get_playbook():
    inventory = ansible.inventory.Inventory(['localhost', '172.30.18.16', '172.30.7.201'])

    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    pb = ansible.playbook.PlayBook(
	 inventory = inventory,
	 playbook = '/root/test.yml',
	 stats = stats, 
	 callbacks = playbook_cb,
	 runner_callbacks = runner_cb,
  	 )
    return pb

@app.route('/inventory/', methods=['GET'])
def inventory():
    res = []
    result = inv.find()
    for r in result:
	res.append(r)
    return json.dumps(res, default=json_util.default)

if __name__ == "__main__": 
    #result = add.delay(3, 2)
    #print result.wait()

    #run = run_playbook.delay(inventory, "/root/test.yml")
    app.run(host='0.0.0.0', debug=True)
