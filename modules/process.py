#!/usr/bin/env python
# encoding: utf-8

"""
# from modules import process
"""

import shlex
from subprocess import PIPE, Popen


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err


##############################################################################

if __name__ == "__main__":
    pass
