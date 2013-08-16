import os
import shlex
from subprocess import call


with open(os.devnull, 'w') as devnull:
    cmd = "command arg1 arg2 ..."
    args = shlex.split(cmd)
    call(args, stdout=devnull, stderr=devnull)
