#!/usr/bin/env python
# encoding: utf-8

"""
# from modules import colored_line_numbers
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

import os
import shlex
from subprocess import call

import config as cfg
from lib import fs
from lib.common import bold
from . import process

pcat = "pygmentize -f terminal256 -O style={0} -g {1}"


def cache_pygmentize():
    """
    The first call of pygmentize is slow, thus we call it upon
    startup in the background.
    """
    fname = "{root}/assets/alap.py".format(root=cfg.ROOT)
    if fs.which("pygmentize") and os.path.isfile(fname):
        with open(os.devnull, 'w') as devnull:
            cmd = pcat.format(cfg.colors[cfg.g.BACKGROUND]["pygmentize_style"], fname)
            args = shlex.split(cmd)
            call(args, stdout=devnull, stderr=devnull)


def pad(text, width, num):
    num_len = len(str(num))
    return "{space}{text}".format(space=(width-num_len)*' ', text=text)


def print_pcat(fname):
    cmd = pcat.format(cfg.colors[cfg.g.BACKGROUND]["pygmentize_style"], fname)
    #
    if cfg.SHOW_LINE_NUMBERS:
        lines = fs.file_len(fname)
        lines_len = len(str(lines))
        width = lines_len + 1
        #
        out = process.get_exitcode_stdout_stderr(cmd)[1]
        out = out.rstrip("\n")
        for i, line in enumerate(out.split("\n"), start=1):
            num_str = bold(str(i), color=cfg.colors[cfg.g.BACKGROUND]["line_numbers"])
            num_str = pad(num_str, width, i)
            print(num_str, line)
    else:
        os.system(cmd)


def cat(fname, o):
    """
    Show file content on stdout.

    If pygmentize is available, show a syntax-highlighted output.
    Otherwise fall back to a normal "cat".
    """
    print(bold("-" * 78))
    doc = o["doc"]
    if doc:
        print(bold(doc))
        print(bold("-" * 78))
    if fs.which("pygmentize"):
        print_pcat(fname)
    else:
        with open(fname) as f:
            for line in f:
                print(line, end='')
    print()

##############################################################################

if __name__ == "__main__":
    pass
