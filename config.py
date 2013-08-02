import os

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

LIGHT, DARK = range(2)
BACKGROUND = DARK
#BACKGROUND = LIGHT
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

