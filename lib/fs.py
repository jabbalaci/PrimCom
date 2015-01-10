#!/usr/bin/env python

"""
file system operations

# from lib.fs import which
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import stat
import sys


def which(program):
    """
    Equivalent of the which command in Python.

    source: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath = os.path.split(program)[0]
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def touch(fname, mode=None):
    """Touch a file.

    If the file doesn't exist, it will be created. In this case
    you can specify its permissions.
    If the file exists, it will be touched. Permissions won't be changed.

    Return True if the file exists, otherwise return False.
    """
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    if not os.path.exists(fname):
        open(fname, 'a').close()
        if mode:
            set_mode_to(fname, mode)
    else:
        os.utime(fname, None)

    return os.path.exists(fname)


def get_oct_mode(fname):
    """Get the permissions of an entry in octal mode.

    The return value is a string (ex. '0600')."""
    entry_stat = os.stat(fname)
    mode = oct(entry_stat[stat.ST_MODE] & 0777)
    return mode


def set_mode_to(fname, permissions):
    """Set the file with the given permissions.

    permissions is given as an octal number (not as a string), ex.: 0700
    Return True if permissions were set successfully, otherwise return False."""
    mode = get_oct_mode(fname)
    if mode != oct(permissions):
        try:
            os.chmod(fname, permissions)
        except OSError:
            print("# cannot chmod the file {0}".format(fname), file=sys.stderr)

    return get_oct_mode(fname) == oct(permissions)


def file_len(fname):
    """
    Number of lines in the file, like "wc -l".
    """
    i = 0
    with open(fname) as f:
        for i, _ in enumerate(f, start=1):
            pass
    return i

#############################################################################

if __name__ == "__main__":
    print(which('bash'))
    print(file_len("na"))
