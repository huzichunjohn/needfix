#!/usr/bin/python
import ansible.playbook
from ansible import callbacks
from ansible import utils
import ansible.inventory
import json

inventory = ansible.inventory.Inventory(["localhost", "172.30.18.16", "172.30.7.201"])

stats = callbacks.AggregateStats()
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
res = ansible.playbook.PlayBook(
    inventory = inventory,
    playbook="/root/test.yml",
    stats=stats,
    callbacks=playbook_cb,
    runner_callbacks=runner_cb,
    ).run()

#for (play_ds, play_basedir) in zip(pb.playbook, pb.play_basedirs):
#    pass
print json.dumps(res, indent=4)

