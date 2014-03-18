#!/usr/bin/env python

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

import os
import re
import shlex
import subprocess as sp
from signal import SIGTERM
from time import sleep

import requests
from bs4 import BeautifulSoup

import config as cfg
from lib import common
from lib.common import exit_signal, remove_non_ascii
from modules.process import get_exitcode_stdout_stderr


def radio(url, stop=False, id=None):
    # "static variables":
    # radio.radio_on, radio.pid, radio.url
    if not hasattr(radio, "on"):
        radio.on = False    # it doesn't exist yet, so initialize it
    radio.id = id
    #
    # for cleaning up:
    if stop:
        if radio.on:
            try:
                os.kill(radio.pid, SIGTERM)
            except OSError:
                pass
            radio.on = False
        return
    #
    if radio.on:
        radio(None, stop=True, id=id)
    #
    if not radio.on:
        common.play_audio(url)
        sleep(.1)
        radio.pid = common.get_pid_by_name(cfg.PLAYER["cmd"])
        radio.on = True
        radio.url = url
        print("Playing:", get_song())
        #print('# radio on')
    else:
        os.kill(radio.pid, SIGTERM)
        radio.on = False
        #print('# radio off')


@exit_signal.connect
def radio_stop(sender):
    radio(None, stop=True)


def read_radio_data():
    """Read the input .csv file."""
    li = []
    dic = {}
    with open("{root}/modules/assets/radio.csv".format(root=cfg.ROOT), 'r') as f:
        for index, line in enumerate(f):
            li.append(line.rstrip("\n").split(';'))
            dic[li[-1][0]] = index

    return li, dic


def radio_player():
    li, dic = read_radio_data()
    for index, e in enumerate(li[1:], start=1):
        print("({pos}) {id:20}[{url}]".format(pos=index, id=e[0], url=e[1]))
    print("[s] stop current radio")
    print("[q] <<")
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if len(inp) == 0:
            continue
        elif inp == 'q':
            return
        elif inp == 's':
            radio(None, stop=True)
            return
        elif inp == 'qq':
            common.my_exit(0)
        try:
            index = int(inp)
            if index < 0:
                raise IndexError
            radio(li[index][1], id=li[index][0])
            return
        except IndexError:
            print("out of range...")
        except ValueError:
            print('Wat?')


def get_song():
    """
    dispatcher
    """
    if radio.id == 'fm95':
        msg = get_song_fm95()
    else:
#        print(radio.url)
        msg = get_stream_title(radio.url)

    return msg


def get_stream_title(url):
    cmd = "mplayer -endpos 0.4 -ao null {url}".format(url=url)
    out = get_exitcode_stdout_stderr(cmd)[1]

    for line in out.split("\n"):
#        print(line)
        if line.startswith('ICY Info:'):
            match = re.search(r"StreamTitle='(.*)';StreamUrl=", line)
            title = match.group(1)
            return title


def get_song_fm95():
    URL = "http://www.radiofm95.hu/netradio_now_fooldal.php"

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text)
        span = soup.find('span', {'class': 'kozepes'})
        font = span.find_all('font')[1]

        return font.text.strip()
    except:
        return 'Some error occurred :('


##############################################################################

if __name__ == "__main__":
    print(get_song_fm95())
