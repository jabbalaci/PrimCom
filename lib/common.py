from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys
from random import shuffle

import psutil

import config as cfg
from . import blinker, fs
from .termcolor import colored

exit_signal = blinker.signal('exit')


def color(text, color, attrs=[]):
    """Produce a colored text for the terminal."""
    return colored(text, color, attrs=attrs)


def bold(text, color=None):
    if color is None:
        color = cfg.colors[cfg.g.BACKGROUND]["bold"]
    return colored(text, color, attrs=['bold'])


def cindex(text, color=None):
    if color is None:
        color = cfg.colors[cfg.g.BACKGROUND]["cindex"]
    return colored(text, color, attrs=['bold'])


def requires(fpath):
    def _decorator(fn):
        if not fs.which(fpath):
            print("Error: {f} doesn't exist".format(f=fpath))
            print("Traceback: {func}() in {src}".format(func=fn.__name__,
                                                        src=__file__))
            my_exit(1)
        #
        def step_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return step_func
        #
    return _decorator


def get_pid_by_name(name):
    # process PIDs that started after this current process
    li = [x for x in psutil.get_pid_list() if x > os.getpid()]
    for pid in li:
        p = psutil.Process(pid)
        if p.name() == name:
            return pid
    #
    return None


def open_url(url, doc=None):
    # Firefox 21.0 (and maybe some other versions too) drops an error
    # message on Ubuntu 13.04: GLib-CRITICAL **: g_slice_set_config: assertion `sys_page_size == 0' failed
    # until it is resolved, I forward the stderr to /dev/null
    if doc:
        print(bold("-" * 78))
        print(bold(doc))
        print(bold("-" * 78))
    #webbrowser.open_new_tab(url)  # use this if the problem is solved
    os.system('firefox -url "{url}" 2>/dev/null &'.format(url=url))  # workaround


@requires(cfg.PLAYER["cmd"])
def play_audio(audio):
    """
    Audio can be a file or an URL stream.
    """
    cmd = '{player} "{audio}" 1>/dev/null 2>&1 &'.format(player=cfg.PLAYER["cmdline"],
                                                         audio=audio)
    os.system(cmd)


def my_exit(error_code=0):
    # threads are subscribed to this signal
    #exit_signal.send()
    #
    sys.exit(error_code)


def remove_non_ascii(text):
    """
    Unicode hell :(
    """
    return ''.join(c for c in text if ord(c) < 128)


def my_shuffle(li):
    """
    Returns a shuffled list.

    random.shuffle shuffles in place and returns None. This way shuffle can be
    used in a chain.
    """
    shuffle(li)
    return li
