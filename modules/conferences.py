import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../lib"))

from signal import SIGTERM          # first this
import common                       # from ../lib
from common import exit_signal, open_url
from config import ROOT             # from ..


def read_conferences_data():
    """Read the input .csv file."""
    li = []
    with open("{root}/modules/assets/conferences.csv".format(root=ROOT), 'r') as f:
        for index, line in enumerate(f):
            li.append(line.rstrip("\n").split(';'))

    return li

def debug(li):
    print "li:"
    print li

def conferences():
    li = read_conferences_data()

#    debug(li)
#    return

    for index, e in enumerate(li[1:], start=1):
        print "({pos}) {id:20}[{url}]".format(pos=index, id=e[0], url=e[1])
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
        elif inp == 'qq':
            common.my_exit(0)
        try:
            index = int(inp)
            if index < 1:
                raise IndexError
            open_url(li[index][1])
            return
        except IndexError:
            print "out of range..."
        except ValueError:
            print 'Wat?'

