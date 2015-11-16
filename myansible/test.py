import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

#import Crypto
#from celery.signals import worker_process_init
#@worker_process_init.connect
#def configure_workers(sender=None, conf=None, **kwargs):
#    Crypto.Random.atfork()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

def get_pb():
    inventory = Inventory(['localhost', '172.30.7.201'])
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)

    pb = PlayBook(playbook='/root/test.yml',
                  callbacks=playbook_cb,
                  runner_callbacks=runner_cb,
                  stats=stats,
                  inventory=inventory,
		  forks = 5
                  #extra_vars=vars,
                  )
    return pb

@celery.task()
def long_task():
    #self.logs = []
    get_pb().run()
    #self.logs.append("finish playbook")
    #self.logs.append(str(r))
    #return self.logs

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    mytask = long_task.apply_async()
    time.sleep(5)
    print mytask.state
