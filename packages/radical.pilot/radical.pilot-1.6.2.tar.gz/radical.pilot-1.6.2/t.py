#!/usr/bin/env python3

import shlex
import radical.pilot as rp
from radical.pilot.task_description import NAMED_ENV


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pmgr  = rp.PilotManager(session=session)
        pdesc = rp.PilotDescription({'resource': 'local.localhost',
                                     'runtime' : 60,
                                     'cores'   : 64})
        pilot = pmgr.submit_pilots(pdesc)


        pilot.prepare_env({
                'scalems_env': {
                    'type': 'virtualenv',
                    'version': '3.8',
                    'setup': [
        'radical.pilot@git+https://github.com/radical-cybertools/radical.pilot.git@project/scalems',
        'scalems@git+https://github.com/SCALE-MS/scale-ms.git@sms-54'
        ]}})

        tmgr  = rp.TaskManager(session=session)

        tmgr.add_pilots(pilot)

        td    = rp.TaskDescription({'executable': 'python3',
                                    'arguments' : ['-c',
                                                   'import radical.pilot as rp;'
                                                   'import scalems;'
                                                   'print(rp.version_detail);'
                                                   'print(scalems.__file__)'],
                                    'named_env' : 'scalems_env'})
        task  = tmgr.submit_tasks(td)
        tmgr.wait_tasks()

        print(task.stdout)

    finally:
        session.close(download=False)


# ------------------------------------------------------------------------------

