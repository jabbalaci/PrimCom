#!/usr/bin/env python

import json
from datetime import datetime
import sys
from collections import OrderedDict
#from pprint import pprint
import os
import config as cfg
from lib import fs
import readline
import random


def read_hdict():
    with open(cfg.JSON) as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def my_hash(bits=96):
    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
    if len(s) < required_length:
        return my_hash(bits)
    else:
        return s


def get_timestamp_from_year_to_second():
    """
    A compact timestamp, e.g. 20110523_234401 (yyyymmdd_hhmmss).
    """
    now = datetime.now()
    date = datetime.date(now)
    time = datetime.time(now)
    template = "{year}{month:02}{day:02}_{hour:02}{minute:02}{second:02}"
    return template.format(year=date.year, month=date.month, day=date.day, hour=time.hour, minute=time.minute, second=time.second)


def get_new_item(hdict):
    myid = my_hash()
    assert myid not in hdict    # its chance is almost zero
    doc = raw_input("doc: ").strip()
    action = raw_input("action: (c)at or (o)pen_url [c/o]? ").strip()
    if action not in ('c', 'o'):
        print "Error: invalid input."
        sys.exit(1)
    action_value = None
    if action == 'c':
        action_text = "cat"
        action_value = raw_input("    cat: ").strip()
        fname = action_value
        if os.path.isfile(fname):
            print "Error: the file {fname} already exists.".format(fname=fname)
            sys.exit(1)
    else:
        action_text = "open_url"
        action_value = raw_input("    open_url: ").strip()
    tags = [tag.strip() for tag in raw_input("tags: ").split(",")]

    hdict[myid] = OrderedDict()
    d = hdict[myid]
    d["doc"] = doc
    d["meta"] = {"date": get_timestamp_from_year_to_second()}
    d["action"] = [action_text, action_value]
    d["tags"] = tags
    d["extra"] = []
    #
    return d, hdict


def save_new_json(d, hdict):
    os.rename(cfg.JSON, cfg.JSON_BAK)
    assert os.path.isfile(cfg.JSON_BAK)
    with open(cfg.JSON, 'w') as f:
        json.dump(hdict, f, indent=4)
    assert os.path.getsize(cfg.JSON) > os.path.getsize(cfg.JSON_BAK)
    print "# added"
    if d["action"][0] == "cat":
        fname = d["action"][1]
        if not os.path.isfile(fname):
            if fs.touch(fname):
                print "# {f} touched".format(f=fname)
                reply = raw_input("Do you want to edit {f} [y/n] (default: yes)? ".format(f=fname)).strip()
                if reply in ('', 'y'):
                    os.system("{ed} {f}".format(ed=cfg.EDITOR, f=fname))


def main():
    hdict = read_hdict()    # it's an OrderedDict
    d, hdict = get_new_item(hdict)
    save_new_json(d, hdict)

#############################################################################

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "interrupted."
