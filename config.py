from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from lib.podium import get_short_fingerprint

# root directory of the application
ROOT = os.path.dirname(os.path.abspath(__file__))

EDITOR = 'vim'
GEDIT = 'gedit'
PLAYER = 'mplayer -ao alsa'    # "-ao alsa" is a workaround to make mplayer quit

ALERT = "{root}/assets/alert.wav".format(root=ROOT)

# data/*.json are loaded automatically
LOAD_JSON = sorted([e for e in os.listdir("{root}/data".format(root=ROOT)) if e.endswith(".json")])

# OR: set manually which databases to load
#LOAD_JSON = [
#    "python.json",
#    "shell.json",
#    "text.json",
#    "urls.json"
#]

class Global(object):
    pass

g = Global()

LIGHT, DARK = range(2)

if get_short_fingerprint() == "d8acf3":
    # my laptop
    g.BACKGROUND = LIGHT
else:
    # anything else
    g.BACKGROUND = DARK

colors = {
    LIGHT: {
        "pygmentize_style": "default",
        "bold": None,    # will be bold black
        "cindex": "blue",
        "cindex_link": "magenta",
        "header": "grey"
    },
    DARK: {
        "pygmentize_style": "native",
        "bold": "white",
        "cindex": "yellow",
        "cindex_link": "magenta",
        "header": "green"
    }
}

# .history file can grow quickly thus we truncate it to N lines upon startup
TRUNCATE_HISTFILE_TO_LINES = 50
