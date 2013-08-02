import os

EDITOR = 'vim'
GEDIT = 'gedit'

ALERT = "assets/alert.wav"

# data/*.json are loaded automatically
LOAD_JSON = sorted([e for e in os.listdir("data") if e.endswith(".json")])

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
