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
from signal import SIGTERM
from time import sleep

import requests
from bs4 import BeautifulSoup

from config import ROOT
from lib import common
from lib.common import exit_signal, remove_non_ascii



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
        radio.pid = common.get_pid_by_name("mplayer")
        radio.on = True
        radio.url = url
        if radio.id in ['slay', 'fm95']:
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
    with open("{root}/modules/assets/radio.csv".format(root=ROOT), 'r') as f:
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
    if radio.id == 'slay':
        msg = get_song_slay()['current']
    elif radio.id == 'fm95':
        msg = get_song_fm95()
    else:
        msg = "Extracting song title is not yet implemented for this radio."

    return msg


def get_song_slay():
    """
    Get info about the current and next song.
    """
    URL = "http://www.slayradio.org/home.php"

    def get_elem(listiterator, index):
        cnt = 0
        for e in listiterator:
            if cnt == index:
                return e
            cnt += 1
    #
    try:
        r = requests.get(URL)
        bs = BeautifulSoup(r.text)
        author = bs.select("html body table tr td div#leftband table tr td.bandContent div#bandVisible_now_playing div#nowplaying strong")[0].text
        div = bs.select("html body table tr td div#leftband table tr td.bandContent div#bandVisible_now_playing div#nowplaying")[0]
        title = get_elem(div.children, 2)
        p = bs.select("html body table tr td div#leftband table tr td.bandContent div#bandVisible_now_playing div#nowplaying p")[0].text
        next_song = p[p.find('Next:'):]
        result = {
            'current': remove_non_ascii("{a}: {t}".format(a=author, t=title)),
            'next': remove_non_ascii(next_song)
        }
    except:
        result = {
            'current': 'Error :(',
            'next': 'Error :('
        }

    return result


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
