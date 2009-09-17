import tempfile
import subprocess
import time
import math

import vdj

# ===================
# = LSF Dispatching =
# ===================

def submit_to_LSF(queue,LSFopfile,cmd_to_submit):
    LSF_params = {'LSFoutput':options.LSFoutput,
                      'queue':options.queue}
    LSF_cmd = r'bsub -q%(queue)s -o%(LSFoutput)s' % LSF_params
    cmd = ' '.join([LSF_cmd,cmd_to_submit])
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    p.wait()
    return p.stdout.read().split('<')[1].split('>')[0]


def wait_for_LSF_jobs(PIDs,interval=30):
    finished = False
    while not finished:
        time.sleep(interval)
        p = subprocess.Popen('bjobs',shell=True,stdout=subprocess.PIPE)
        p.wait()
        status = p.stdout.read().split('\n')
        if status[0].split()[0] != 'JOBID':
            finished = False
            continue
        runningprocesses = [line.split()[0] for line in status if line.split() != [] and line.split()[0] != 'JOBID']
        finished = True
        for pid in PIDs:
            if pid in runningprocesses:
                finished = False
