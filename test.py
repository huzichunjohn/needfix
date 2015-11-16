#!/usr/bin/python
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils

stats = callbacks.AggregateStats()
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)

pb = PlayBook(playbook='/root/test.yml', 
              callbacks=playbook_cb,
              runner_callbacks=runner_cb,
              stats=stats,
              )
pb.run()










