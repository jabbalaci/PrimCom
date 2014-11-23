from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

from lib.podium import get_short_fingerprint


__author__ = "Laszlo Szathmary (jabba.laci@gmail.com)"
__version__ = "0.4.7"
__date__ = "20141123"
__copyright__ = "Copyright (c) 2013--2014 Laszlo Szathmary"
__license__ = "GPL"


# root directory of the application
ROOT = os.path.dirname(os.path.abspath(__file__))

EDITOR = "vim"
GEDIT = 'gedit'
PLAYER = {
    "cmd":      "mplayer",
    "cmdline":  "mplayer -ao alsa"   # a workaround to make mplayer quit
}
ALERT = "{root}/assets/alert.wav".format(root=ROOT)

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'

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

if get_short_fingerprint() in ("d8acf3", "a2b110"):
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
        "header": "grey",
        "line_numbers": "grey",
    },
    DARK: {
        "pygmentize_style": "native",
        "bold": "white",
        "cindex": "yellow",
        "cindex_link": "magenta",
        "header": "green",
        "line_numbers": "yellow",
    }
}

# When printing the content of a file, show line numbers?
SHOW_LINE_NUMBERS = True
#SHOW_LINE_NUMBERS = False

# .history file can grow quickly thus we truncate it to N lines upon startup
TRUNCATE_HISTFILE_TO_LINES = 20

#############################################################################

if __name__ == "__main__":
    print(get_short_fingerprint())
