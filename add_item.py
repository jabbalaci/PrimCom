#!/usr/bin/env python

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import getpass
import json
import os
import readline
import sys
from collections import OrderedDict
from datetime import datetime

import config as cfg
from lib import fs
from lib.simpleflake import simpleflake


def get_timestamp_from_year_to_second():
    """
    A compact timestamp, e.g. 20110523_234401 (yyyymmdd_hhmmss).
    """
    now = datetime.now()
    date = datetime.date(now)
    time = datetime.time(now)
    template = "{year}{month:02}{day:02}_{hour:02}{minute:02}{second:02}"
    return template.format(year=date.year, month=date.month, day=date.day,
                           hour=time.hour, minute=time.minute, second=time.second)


def create_db(db):
    dbfile = "{root}/data/{db}.json".format(root=cfg.ROOT, db=db)
    if not os.path.isfile(dbfile):
        with open(dbfile, "w") as f:
            f.write("{}")    # empty dict.
    else:
        print("Warning! The file {db} already exists.".format(db=dbfile))
    #
    dbdir = "{root}/data/{db}".format(root=cfg.ROOT, db=db)
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    else:
        print("Warning! The dir. {db} already exists.".format(db=dbdir))


def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


def get_db():
    li = [e for e in os.listdir("{root}/data".format(root=cfg.ROOT)) if e.endswith(".json") and e != "urls.json"]
    for index, db in enumerate(li, start=1):
        print("[{i}] {db}".format(i=index, db=strip_end(db, ".json")))
    print("[n] new...")
    print("[q] quit")
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)
        if len(inp) == 0:
            continue
        elif inp in ('q', 'qq'):
            sys.exit(0)
        elif inp == "n":
            db = raw_input("New DB: ").strip()
            if db:
                create_db(db)
        else:
            try:
                index = int(inp) - 1
                if index < 0:
                    raise IndexError
                db = li[index]
            except IndexError:
                print("out of range...")
            except ValueError:
                print('Wat?')
        #
        if db:
            break
    #
    return strip_end(db, ".json")


def get_new_item():
    myid = simpleflake()
    doc = raw_input("doc: ").strip()
    action = raw_input("action: (c)at or (o)pen_url [c/o]? ").strip()
    if action not in ('c', 'o'):
        print("Error: invalid input.")
        sys.exit(1)
    action_value = None
    if action == 'c':
        action_text = "cat"
        print("Choose category:")
        db = get_db()
        action_value = raw_input("  filename: ").strip()
        action_value = "{db}/{av}".format(db=db, av=action_value)
        fname = "{root}/data/{db}/{f}".format(root=cfg.ROOT, db=db, f=action_value)
        if os.path.isfile(fname):
            print("Error: the file {fname} already exists.".format(fname=fname))
            sys.exit(1)
        dbfile = "{root}/data/{db}.json".format(root=cfg.ROOT, db=db)
    else:
        action_text = "open_url"
        action_value = raw_input("  open_url: ").strip()
        db = "urls"
        dbfile = "{root}/data/urls.json".format(root=cfg.ROOT)
    #
    tags = [tag.strip() for tag in raw_input("tags: ").split(",")]

    with open(dbfile) as f:
        dbdict = json.load(f, object_pairs_hook=OrderedDict)

    dbdict[myid] = OrderedDict()
    d = dbdict[myid]
    d["doc"] = doc
    d["meta"] = {
        "date": get_timestamp_from_year_to_second(),
        "author": getpass.getuser()
    }
    d["action"] = [action_text, action_value]
    d["tags"] = tags
    d["extra"] = []
    #
    return d, dbdict, db


def save_new_json(d, hdict, db):
    orig = "{root}/data/{db}.json".format(root=cfg.ROOT, db=db)
    bak = "{root}/tmp/{db}.json.bak".format(root=cfg.ROOT, db=db)
    #
    os.rename(orig, bak)
    assert os.path.isfile(bak)
    with open(orig, 'w') as f:
        json.dump(hdict, f, indent=4)
    assert os.path.getsize(orig) > os.path.getsize(bak)
    print("# added to {db}.json".format(db=db))
    if d["action"][0] == "cat":
        fname = "{root}/data/{f}".format(root=cfg.ROOT, f=d["action"][1])
        if not os.path.isfile(fname):
            if fs.touch(fname):
                print("# {f} touched".format(f=fname))
                reply = raw_input("Do you want to edit {f} [y/n] (default: yes)? ".format(f=fname)).strip()
                if reply in ('', 'y'):
                    os.system("{ed} {f}".format(ed=cfg.EDITOR, f=fname))


def main():
    d, hdict, db = get_new_item()
    save_new_json(d, hdict, db)

#############################################################################

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("interrupted.")
