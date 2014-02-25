#!/usr/bin/env python

"""
Copy text to clipboards (to both of them).
This solution here is specific to Linux.

For a platform independent solution, you can check out
https://github.com/asweigart/mapitpy/blob/master/pyperclip.py
(I didn't try it).

# from lib.clipboard import text_to_clipboards
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import shlex
import subprocess
from subprocess import PIPE, Popen, STDOUT

from termcolor import colored


def text_to_clipboards(text, verbose=True):
    """Copy text to both clipboards."""
    to_primary(text)
    to_clipboard(text)
    if verbose:
        print(bold("# copied to the clipboards"))


def bold(text, color='white'):
    return colored(text, color, attrs=['bold'])


def get_simple_cmd_output(cmd, stderr=STDOUT):
    """Execute a simple external command and get its output.

    The command contains no pipes. Error messages are
    redirected to the standard output by default.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

#############################################################################

def to_primary(text):
    """Write text to 'primary'."""
    xsel_proc = subprocess.Popen(['xsel', '-pi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(text)


def to_clipboard(text):
    """Write text to 'clipboard'."""
    xsel_proc = subprocess.Popen(['xsel', '-bi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(text)

#############################################################################

def read_primary():
    """Read content of 'primary'."""
    cmd = 'xsel -po'
    return get_simple_cmd_output(cmd)


def read_clipboard():
    """Read content of 'clipboard'."""
    cmd = 'xsel -bo'
    return get_simple_cmd_output(cmd)

#############################################################################

if __name__ == "__main__":
    text = "this should go on the clipboards"
    print(text)
    text_to_clipboards(text)
