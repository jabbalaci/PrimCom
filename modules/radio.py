#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../lib"))

from time import sleep
from signal import SIGTERM          # first this
import common                       # from ../lib
from common import exit_signal, remove_non_ascii
from config import ROOT             # from ..

from bs4 import BeautifulSoup
import requests

SLAY = "http://www.slayradio.org/home.php"


def radio(url, stop=False):
    # "static variables":
    # radio.radio_on, radio.pid, radio.url
    if not hasattr(radio, "on"):
        radio.on = False    # it doesn't exist yet, so initialize it
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
        radio(None, stop=True)
    #
    if not radio.on:
        common.play_audio(url)
        sleep(.1)
        radio.pid = common.get_pid_by_name("mplayer")
        radio.on = True
        radio.url = url
        if "slayradio" in url:
            print "Playing:", get_song()['current']
        #print '# radio on'
    else:
        os.kill(radio.pid, SIGTERM)
        radio.on = False
        #print '# radio off'


@exit_signal.connect
def radio_stop(sender):
    radio(None, stop=True)


def read_radio_data():
    """Read the input .csv file."""
    li = []
    dic = {}
    with open("{root}/modules/assets/radio.csv".format(root=ROOT), 'r') as f:
        for index, line in enumerate(f):
            li.append(line.rstrip("\n").split(';'))
            dic[li[-1][0]] = index

    return li, dic


def radio_player():
    li, dic = read_radio_data()
    for index, e in enumerate(li[1:], start=1):
        print "({pos}) {id:20}[{url}]".format(pos=index, id=e[0], url=e[1])
    print "[s] stop current radio"
    print "[q] <<"
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print
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
            radio(li[index][1])
            return
        except IndexError:
            print "out of range..."
        except ValueError:
            print 'Wat?'


def get_song():
    """
    Get info about the current and next song.
    """
    def get_elem(listiterator, index):
        cnt = 0
        for e in listiterator:
            if cnt == index:
                return e
            cnt += 1
    #
    try:
        r = requests.get(SLAY)
        bs = BeautifulSoup(r.text)
        author = bs.select("html body table tr td div#leftband table tr td.bandContent div#bandVisible_now_playing div#nowplaying strong")[0].text
        div = bs.select("html body table tr td div#leftband table tr td.bandContent div#bandVisible_now_playing div#nowplaying")[0]
        title = get_elem(div.children, 2)
        p = bs.select("html body table tr td div#leftband table tr td.bandContent div#bandVisible_now_playing div#nowplaying p")[0].text
        next_song = p[p.find('Next:'):]
        result = {
            'current' : remove_non_ascii("{a}: {t}".format(a=author, t=title)),
            'next' : remove_non_ascii(next_song)
        }
    except:
        result = {
            'current' : 'Error :(',
            'next' : 'Error :('
        }

    return result

##############################################################################

if __name__ == "__main__":
    print get_song()
