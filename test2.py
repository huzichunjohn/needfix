from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

class PlaybookRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):
    def __init__(self, stats, verbose=None):
        super(PlaybookRunnerCallbacks, self).__init__(stats, verbose)
	print "__init__"
	#self.task = task

    def on_ok(self, host, host_result):
        super(PlaybookRunnerCallbacks, self).on_ok(host, host_result)
	print "on_ok"

    def on_unreachable(self, host, results):
        output = super(PlaybookRunnerCallbacks, self).on_unreachable(host, results)
	print output
	
    def on_failed(self, host, results, ignore_errors=False):
        super(PlaybookRunnerCallbacks, self).on_failed(host, results, ignore_errors)
	
#
#    def runner_on_skipped(self, host, item=None):
#	super(PlaybookRunnerCallbacks, self).runner_on_skipped(self, host, item)
#        print "runner_on_skipped"


class PlaybookCallbacks(callbacks.PlaybookCallbacks):
    def __init__(self, verbose=False):
        super(PlaybookCallbacks, self).__init__(verbose);
	print "__init__"	

    def on_setup(self):
        super(PlaybookCallbacks, self).on_setup()
	print "on_setup"	

    def on_task_start(self, name, is_conditional):
        super(PlaybookCallbacks, self).on_task_start(name, is_conditional)
	print "on_task_start"

    def playbook_on_task_start(self, name, is_conditional):
	super(PlaybookCallbacks, self).playbook_on_task_start(self, name, is_conditional)
	print "playbook_on_task_start"



class CallbackModule(object):
    def __init__(self):
	pass

    def _log_event(self, event, **event_data):
        if self.callback_consumer_port:
            self._post_job_event_queue_msg(event, event_data)
        else:
            self._post_rest_api_event(event, event_data)

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self._log_event('runner_on_failed', host=host, res=res,
                        ignore_errors=ignore_errors)

    def runner_on_ok(self, host, res):
        self._log_event('runner_on_ok', host=host, res=res)

    def runner_on_error(self, host, msg):
        self._log_event('runner_on_error', host=host, msg=msg)

    def runner_on_skipped(self, host, item=None):
        self._log_event('runner_on_skipped', host=host, item=item)

    def runner_on_unreachable(self, host, res):
        self._log_event('runner_on_unreachable', host=host, res=res)

    def runner_on_no_hosts(self):
        self._log_event('runner_on_no_hosts')

    def runner_on_async_poll(self, host, res, jid, clock):
        self._log_event('runner_on_async_poll', host=host, res=res, jid=jid,
                        clock=clock)

    def runner_on_async_ok(self, host, res, jid):
        self._log_event('runner_on_async_ok', host=host, res=res, jid=jid)

    def runner_on_async_failed(self, host, res, jid):
        self._log_event('runner_on_async_failed', host=host, res=res, jid=jid)

    def runner_on_file_diff(self, host, diff):
        self._log_event('runner_on_file_diff', host=host, diff=diff)


inventory = Inventory(['localhost']) 
stats = callbacks.AggregateStats()

def get_pb():
    runner_cb = PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
    playbook_cb = PlaybookCallbacks(verbose=utils.VERBOSITY)

    pb = PlayBook(playbook='/root/test.yml', 
                  callbacks=playbook_cb,
                  runner_callbacks=runner_cb,
                  stats=stats,
                  inventory=inventory,
                  )
    return pb

if __name__ == '__main__':
    get_pb().run()

