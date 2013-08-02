#!/usr/bin/env python

"""
PrimCom
=======

"Boost your productivity with PrimCom."

Manage and access your personal knowledge base easily.


Some rules:
-----------
* Every key has an associated value, an object.
  This object must have a "doc", an "action", and a "tags" key.
* Tags cannot start with an underscore (they have a special meaning).
* The first tag is special, it will be used elsewhere too.
  So choose the very first tag carefully and make sure it's informative.
* Tags must be at least 2 characters long.
  Also, they cannot be numbers (numbers have a special meaning).
"""

import sys
# to be able to import blinker
sys.path.insert(0, "./lib/")

import os
import re
import json
from collections import OrderedDict
#from pprint import pprint
#import webbrowser
from lib.termcolor import colored
from lib.clipboard import text_to_clipboards
import requests
import config as cfg
from lib import fs
import readline
import psutil    # sudo apt-get install python-psutil
from signal import SIGTERM        # first this
from lib.blinker import signal    # then this
from time import sleep
import atexit
from threading import Thread

__author__ = "Laszlo Szathmary (jabba.laci@gmail.com)"
__version__ = "0.2.7"
__date__ = "20130802"
__copyright__ = "Copyright (c) 2013 Laszlo Szathmary"
__license__ = "GPL"

BACKGROUND = cfg.BACKGROUND

pcat = "pygmentize -f terminal256 -O style={0} -g {1}"
PLAYER='mplayer -ao alsa'    # "-ao alsa" is a workaround to make mplayer quit

# If you want the command "less" to use colors, follow the steps in this post:
# https://ubuntuincident.wordpress.com/2013/06/05/syntax-highlighted-less-in-command-line/

# these are all re-set in read_json()
hdict = OrderedDict()      # will be set later
tag2keys = OrderedDict()   # will be set later
#search_result = []         # will be updated after each search
last_key = None            # will be updated after each command
autocomplete_commands = [] # will be filled later (used for autocomplete)

pid_checker = None         # it'll be a PidChecker object

dependencies = {
    # command: package installation
    'pygmentize': 'sudo apt-get install python-pygments',
    'xsel': 'sudo apt-get install xsel',
}

LOAD_JSON = cfg.LOAD_JSON

exit_signal = signal('exit')


#############
## Helpers ##
#############

class NoLastKeyError(Exception):
    pass

def color(text, color, attrs=[]):
    """Produce a colored text for the terminal."""
    return colored(text, color, attrs=attrs)


def bold(text, color=None):
    if color is None:
        color=cfg.colors[BACKGROUND]["bold"]
    return colored(text, color, attrs=['bold'])


def cindex(text, color=None):
    if color is None:
        color=cfg.colors[BACKGROUND]["cindex"]
    return colored(text, color, attrs=['bold'])


def check_dependencies():
    for prg in dependencies:
        if not fs.which(prg):
            print "Warning: {0} is not available.".format(prg)
            print "tip: {0}".format(dependencies[prg])


def header():
    s = "PrimCom {v}".format(v=__version__)
    size = len(s)
    horizontal = '+' + '-' * (size+2) + '+'
    col = cfg.colors[BACKGROUND]["header"]
    print bold(horizontal, col)
    print bold('| ' + s + ' |', col)
    print bold(horizontal, col)


def requires(fpath):
    def _decorator(fn):
        if not fs.which(fpath):
            print "Error: {f} doesn't exist".format(f=fpath)
            print "Traceback: {func}() in {src}".format(func=fn.__name__, src=__file__)
            my_exit(1)
        #
        def step_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return step_func
    return _decorator


def completer(text, state):
    # for autocomplete
    if re.search(r'^\d+\.', text):    # if it starts with a number
        pos = text.find('.')
        num = text[:pos]
        text = text[pos+1:]
        options = [x for x in autocomplete_commands if x.startswith(text)]
        try:
            return num + '.' + options[state]
        except IndexError:
            return None
    else:    # normal case
        options = [x for x in autocomplete_commands if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None


def setup_history_and_tab_completion():
    histfile = ".history"
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    if os.path.isfile(histfile):
        readline.read_history_file(histfile)
    atexit.register(readline.write_history_file, histfile)


def get_db_by_key(key):
    """
    Having a key, tell which DB the item belongs to.
    """
    o = hdict[key]
    action = o["action"]
    if action[0] == "cat":
        val = action[1]
        return val[:val.find('/')]
    #
    return None

#############
## Classes ##
#############

class SearchHits(object):
    inp = None
    hits = []


    @staticmethod
    def reset():
        SearchHits.inp = None
        SearchHits.hits = []


    @staticmethod
    def show_hint(inp):
        SearchHits.reset()
        #
        SearchHits.inp = inp.lower()
        for o in hdict.itervalues():
            for t in o["tags"]:
                if inp in t.lower():
                    #li.append(t)
                    SearchHits.add(t)
        #
        #li = remove_duplicates_keep_order(li)
        SearchHits.remove_duplicates_and_keep_order()
        #
        #if li:
        if SearchHits.hits:
            #show_tag_list(li)
            SearchHits.show_tag_list()
        else:
            print 'Wat?'


    @staticmethod
    def add(tag):
        SearchHits.hits.append(Hit(tag))


    @staticmethod
    def remove_duplicates_and_keep_order():
        my_set = set()
        cleaned = []
        for hit in SearchHits.hits:
            if hit.tag not in my_set:
                cleaned.append(hit)
                my_set.add(hit.tag)
        #
        SearchHits.hits = cleaned


    @staticmethod
    def show_tag_list(li=None):
        if li:
            SearchHits.reset()
            for tag in li:
                SearchHits.add(tag)

        for index, e in enumerate(SearchHits.hits, start=1):
            if index > 1:
                sys.stdout.write(', ')
            sys.stdout.write(e.to_str(index))
        print

##########

class Hit(object):
    def __init__(self, tag, key=None):
        if not key:     # normal "constructor":
            self.tag = tag
            self.keys = tag2keys[tag]
            if len(self.keys) == 1:
                self.o = hdict[self.keys[0]]
            else:
                self.o = None
        else:           # alternative "constructor":
            self.keys = [key]
            self.o = hdict[key]
            self.tag = self.o["tags"][0]

    def __str__(self):
        return self.tag

    def is_link(self):
        if self.o and self.o["action"][0] == "open_url":
            return True
        #
        return False

    def inspect(self, what):
        o = self.o
        if o:
            if what in ('doc', 'action', 'tags'):
                print o[what]
            elif what == 'json':
                print json.dumps(o, indent=4)
            elif what in ('url', 'link'):
                if self.is_link():
                    print o["action"][1]
            elif what == 'key':
                print self.keys[0]
            elif what == 'edit':
                if len(self.keys) == 1:
                    edit(self.keys[0])
            elif what == 'jet':
                if len(self.keys) == 1:
                    edit_entry(self.keys[0])
            else:
                print "Wat?"

    def to_str(self, index):
        s = ""
        if self.is_link():
            s += cindex('({0}) '.format(index), color=cfg.colors[BACKGROUND]["cindex_link"])
        else:
            s += cindex('({0}) '.format(index))
        s += self.tag
        if len(self.keys) > 1:
            s += '...'
        return s

##########

class PidChecker(Thread):
    def __init__(self):
        super(PidChecker, self).__init__()
        self.checklist = set()
        self.running = True
        exit_signal.connect(self.terminate)

    def add(self, pid):
        try:
            pid = int(pid)
        except ValueError:
            print 'Hm?'
            return
        # else
        try:
            self.checklist.add(psutil.Process(pid))
            if not self.isAlive():
                self.start()
        except psutil._error.NoSuchProcess:
            print 'Warning: no such PID.'

    def remove(self, pid):
        try:
            pid = int(pid)
        except ValueError:
            print 'Hm?'
            return
        # else
        for proc in self.checklist:
            if pid == proc.pid:
                self.checklist.remove(proc)
                break
        else:
            print 'Warning: no such PID.'


    def stop(self):
        self.running = False

    def terminate(self, data):
        if self.isAlive():
            self.stop()
            self.join()

    def contents(self):
        if not self.checklist:
            print '<empty>'
        else:
            for p in sorted(self.checklist, key=lambda p: p.pid):
                print '*', p

    def run(self):
        while self.running:
            pids = set(psutil.get_pid_list())
            try:
                for proc in self.checklist:
                    pid = proc.pid
                    if pid not in pids:
                        play_beep()
                        notify_send("Process with PID {pid} stopped.".format(pid=pid))
                        self.checklist.remove(proc)
            except RuntimeError:
                continue
            sleep(1)

pid_checker = PidChecker()

##########
## Core ##
##########

def process(d):
    t2k = OrderedDict()    # tag2keys
    #
    for k in d.iterkeys():
        o = d[k]
        if not(("doc" in o) and ("action" in o) and ("tags" in o)):
            print "Error: '{k}' must have doc, action, and tags.".format(k=k)
            my_exit(1)
        if len(o["doc"]) == 0:
            print "Error: '{k}' must have a valid doc.".format(k=k)
            my_exit(1)
        if len(o["tags"]) == 0:
            print "Error: '{k}' must have at least one tag.".format(k=k)
            my_exit(1)
        for t in o["tags"]:
            t = t.strip()
            if t[0] == '_':
                print "Error: the tag {tag} cannot start with an underscore.".format(tag=t)
                my_exit(1)
            if len(t) == 1:
                print "Error: the tag '{t}' in {k} is too short.".format(t=t, k=k)
                my_exit(1)
            if t in t2k:
                t2k[t].append(k)
            else:
                t2k[t] = [k]
            #autocomplete_commands.append("_"+t.lower())
    #
    return t2k


def read_json(verbose=True):
    global hdict, tag2keys, search_result, last_key
    #
    hdict = OrderedDict()
    tag2keys = OrderedDict()
    search_result = []
    last_key = None
    #
    for db in LOAD_JSON:
        tmp = OrderedDict()
        with open("data/"+db) as f:
            tmp = json.load(f, object_pairs_hook=OrderedDict)
        for k in tmp:
            hdict[k] = tmp[k]
        if verbose:
            print "# {db} reloaded".format(db=db)
    #
    # sort hdict items by date
    hdict = OrderedDict(sorted(hdict.iteritems(), key=lambda x: x[1]["meta"]["date"]))
    #
    tag2keys = process(hdict)


def cat(fname, o):
    """
    Show file content on stdout.

    If pygmentize is available, show a syntax-highlighted output.
    Otherwise fall back to a normal "cat".
    """
    fname = "data/" + fname
    #
    print bold("-" * 78)
    doc = o["doc"]
    if doc:
        print bold(doc)
        print bold("-" * 78)
    if fs.which("pygmentize"):
        os.system(pcat.format(cfg.colors[BACKGROUND]["pygmentize_style"], fname))
    else:
        with open(fname) as f:
            for line in f:
                print line,
    print
    #
    process_extras(fname, o)


def process_extras(fname, o):
    """
    Currently implemented extras:
    * cb()    -> copy file content to the clipboards
    """
    extra = o.get("extra")
    if not extra:
        return
    # else
    for e in extra:
        if e == "cb()":
            text_to_clipboards(open(fname).read().rstrip("\n"))
        else:
            print "Warning: unknown extra option: {e}".format(e=e)


def open_url(url, doc=None):
    # Firefox 21.0 (and maybe some other versions too) drops an error
    # message on Ubuntu 13.04: GLib-CRITICAL **: g_slice_set_config: assertion `sys_page_size == 0' failed
    # until it is resolved, I forward the stderr to /dev/null
    #webbrowser.open_new_tab(url)    ## use this if the problem is solved
    if doc:
        print bold("-" * 78)
        print bold(doc)
        print bold("-" * 78)
    os.system('firefox -url "{url}" 2>/dev/null'.format(url=url))    ## workaround


def extract_urls(fname):
    with open(fname) as f:
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())


def show_urls(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == 'cat':
        fname = "data/"+action[1]
    else:
        return

    # OK, we have the fname
    li = extract_urls(fname)
    for index, url in enumerate(li, start=1):
        print "[{i}] {url}".format(i=index, url=url)
    print "[q] <<"
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print
            return None
        if len(inp) == 0:
            continue
        if inp == 'q':
            return None
        if inp == 'qq':
            my_exit(0)
        try:
            index = int(inp)-1
            if index < 0:
                raise IndexError
            open_url(li[index])
            return
        except IndexError:
            print "out of range..."
        except ValueError:
            print 'Wat?'


def subcommand(li):
    def is_link(k):
        return Hit(tag=None, key=k).is_link()

    for index, k in enumerate(li, start=1):
        if is_link(k):
            pre = cindex('[{0}]'.format(index), color=cfg.colors[BACKGROUND]["cindex_link"])
        else:
            pre = cindex('[{0}]'.format(index))
        print "{pre} {main_tag} ({doc})".format(
            pre=pre,
            main_tag=hdict[k]["tags"][0],
            doc=hdict[k]["doc"]
        )
    print "[q] <<"
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print
            return None
        if len(inp) == 0:
            continue
        if inp == 'q':
            return None
        if inp == 'qq':
            my_exit(0)
        try:
            index = int(inp)-1
            if index < 0:
                raise IndexError
            perform_action(li[index])
            return
        except IndexError:
            print "out of range..."
        except ValueError:
            print 'Wat?'


def reddit():
    li = [
        '/r/python',
        '/r/programming',
    ]
    for index, subreddit in enumerate(li, start=1):
        print "[{i}] {sr}".format(i=index, sr=subreddit)
    print "[q] <<"
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print
            return None
        if len(inp) == 0:
            continue
        if inp == 'q':
            return None
        if inp == 'qq':
            my_exit(0)
        try:
            index = int(inp)-1
            if index < 0:
                raise IndexError
            url = "http://www.reddit.com{sr}".format(sr=li[index])
            open_url(url)
            return
        except IndexError:
            print "out of range..."
        except ValueError:
            print 'Wat?'


def get_pid_by_name(name):
    # process PIDs that started after this current process
    li = [x for x in psutil.get_pid_list() if x > os.getpid()]
    for pid in li:
        p = psutil.Process(pid)
        if p.name == name: 
            return pid
    #
    return None


@requires('mplayer')
def play_audio(audio):
    """
    Audio can be a file or an URL stream.
    """
    cmd = '{mplayer} "{audio}" 1>/dev/null 2>&1 &'.format(mplayer=PLAYER, audio=audio)
    os.system(cmd)


def radio(url, stop=False):
    # "static variables":
    # slay.radio_on, slay.pid
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
        play_audio(url)
        sleep(.1)
        radio.pid = get_pid_by_name("mplayer")
        radio.on = True
        radio.url = url
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
    with open("assets/stations.csv", 'r') as f:
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
            my_exit(0)
        try:
            index = int(inp)
            if index < 0:
                raise IndexError
            #print '#', li[index]
            radio(li[index][1])
            return
        except IndexError:
            print "out of range..."
        except ValueError:
            print 'Wat?'


def play_beep():
    play_audio(cfg.ALERT)


def notify_send(msg):
    logo = os.path.abspath("assets/logo.xpm")
    main = "PrimCom Alert"
    sub = msg
    cmd = 'notify-send -i {logo} "{main}" "{sub}"'.format(logo=logo, main=main, sub=sub)
    os.system(cmd)


def watch_pid():
    pid_checker.contents()
    try:
        pid = int(raw_input("PID: ").strip())
    except ValueError:
        print 'Wat?'
        return
    except (KeyboardInterrupt, EOFError):
        print
        return
    # else
    if pid not in psutil.get_pid_list():
        print 'Warning: no such PID.'
        return
    # else
    pid_checker.add(pid)


def pid_alert():
    text = """
(1) ps
(2) adjust alert volume
(3) set pid to watch (add:<pid>, remove:<pid>)
(4) list of watched processes (d)
[m] this menu
[q] <<
""".strip()
    print text
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
            my_exit(0)
        elif inp == 'm':
            print text
        elif inp.startswith('!'):
            cmd = inp[1:]
            os.system(cmd)
        elif inp in ('1', 'ps'):
            os.system("ps ux")
        elif inp == '2':
            play_beep()
        elif inp == '3':
            watch_pid()
        elif inp in ('4', 'd'):
            pid_checker.contents()
        elif inp.startswith('add:'):
            pid_checker.add(inp[inp.find(':')+1:])
        elif inp.startswith('remove:'):
            pid_checker.remove(inp[inp.find(':')+1:])
        else:
            print 'Wat?'


def debug():
    watch_pid()


def command(inp):
    li = tag2keys[inp]
    if len(li) > 1:
        subcommand(li)
    else:
        perform_action(li[0])


def perform_action(key):
    global last_key
    last_key = key
    #
    o = hdict[key]
    action = o["action"]
    verb = action[0]
    if verb == 'cat':
        cat(action[1], o)
    elif verb == 'open_url':
        open_url(action[1], o["doc"])
    else:
        print "Error: unknown action: {a}.".format(a=verb)
        my_exit(1)


def view_edit_json(key):
    db = get_db_by_key(key)
    os.system("{ed} {f}".format(ed=cfg.EDITOR, f="data/{db}.json".format(db=db)))


def to_clipboards(key):
    if fs.which("xsel"):
        o = hdict[key]
        #
        action = o["action"]
        verb = action[0]
        if verb == 'cat':
            with open("data/"+action[1]) as f:
                text_to_clipboards(f.read().rstrip("\n"))
    else:
        print "Warning: xsel is not installed, cannot copy to clipboards."


def show_doc(key):
    o = hdict[key]
    print o["doc"]


@requires(cfg.EDITOR)
def edit(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == 'cat':
        os.system("{ed} {fname}".format(ed=cfg.EDITOR, fname="data/"+action[1]))


@requires(cfg.GEDIT)
def gedit(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == 'cat':
        os.system("{ed} {fname} &".format(ed=cfg.GEDIT, fname="data/"+action[1]))


def less(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == 'cat':
        os.system("less {fname}".format(fname="data/"+action[1]))


def first_google_hit(keyword):
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + keyword
    r = requests.get(url)
    d = r.json()
    return d["responseData"]["results"][0]["url"]


def cmd_google(keyword):
    open_url("https://www.google.com/search?q="+keyword)


def cmd_youtube(keyword):
    open_url("https://www.youtube.com/results?search_query="+keyword)


def cmd_go1(keyword, site=None):
    if not site:
        q = keyword
    else:
        q = "site:{site} {kw}".format(site=site, kw=keyword)
    #
    url = first_google_hit(q)
    open_url(url)


def shorten_url(long_url):
    try:
        url = "https://www.googleapis.com/urlshortener/v1/url"
        data = {"longUrl": long_url}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        short = r.json()["id"]
        print short
        text_to_clipboards(short)
    except:
        print "Hmm, strange..."


def add_item():
    os.system("python ./add_item.py")


def edit_entry(key):
    db = get_db_by_key(key)
    dbfile = "data/{db}.json".format(db=db)
    d = OrderedDict()
    d[key] = hdict[key]
    tmpfile = 'tmp/temp.{pid}.json'.format(pid=os.getpid())
    with open(tmpfile, 'w') as f:
        json.dump(d, f, indent=4)
    assert os.path.isfile(tmpfile)
    os.system("{ed} {fname}".format(ed=cfg.EDITOR, fname=tmpfile))
    #
    with open(tmpfile) as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
    with open(dbfile) as f:
        dbdict = json.load(f, object_pairs_hook=OrderedDict)
    #
    dbdict[key] = d[key]
    os.unlink(tmpfile)
    #
    tmpfile = "tmp/{db}.json.bak".format(db=db)
    os.rename(dbfile, tmpfile)
    assert os.path.isfile(tmpfile)
    with open(dbfile, 'w') as f:
        json.dump(dbdict, f, indent=4)
    print "# edited"
    read_json()


def show_my_ip():
    r = requests.get("http://jsonip.com/")
    ip = r.json()["ip"]
    print ip
    text_to_clipboards(ip)


def version():
    text = """
PrimCom {v} ({date}) by Laszlo Szathmary (jabba.laci@gmail.com), 2013
""".format(v=__version__, date=__date__)
    print text.strip()


@requires(cfg.EDITOR)
def menu():
    global BACKGROUND
    #
    while True:
        try:
            inp = raw_input(bold('pc> ')).strip()
        except (KeyboardInterrupt, EOFError):
            print
            my_exit(0)
        if len(inp) == 0:
            continue
        #if len(inp) > 1 and inp[0] == '_':    # ??? remove?
        #    inp = inp[1:]
        #
        if inp in ('h', 'help()'):
            info()
        elif inp in ('q', 'qq', 'quit()', 'exit()'):
            my_exit(0)
        elif inp in ('c', 'clear()'):
            os.system('clear')
            header()
        elif inp in ('light()', 'dark()'):
            if inp == 'light()':
                BACKGROUND = cfg.LIGHT
            else:
                BACKGROUND = cfg.DARK
        elif inp in ('t', 'tags()', 'all()', 'd'):
            SearchHits.show_tag_list(tag2keys.keys())
        elif inp == 'p':
            os.system("python")
        elif inp == 'last()':
            print last_key
        elif inp == '!!':
            if last_key:
                perform_action(last_key)
        elif inp.startswith('!'):
            cmd = inp[1:]
            os.system(cmd)
        elif inp == 'edit()':
            if last_key:
                edit(last_key)
        elif inp == 'gedit()':
            if last_key:
                gedit(last_key)
        elif inp == 'less()':
            if last_key:
                less(last_key)
        elif inp in ('urls()', 'links()'):
            if last_key:
                show_urls(last_key)
        elif inp in ('cb()', 'tocb()'):
            if last_key:
                to_clipboards(last_key)
        elif inp == "doc()":
            if last_key:
                show_doc(last_key)
        elif inp == 'json.reload()':
            read_json()
        elif inp in ('json.view()', 'json.edit()'):
            if last_key:
                view_edit_json(last_key)
                read_json()
        elif inp in ("json.edit(this)", "jet()"):
            if last_key:
                edit_entry(last_key)
        elif inp == 'reddit()':
            reddit()
        elif inp == 'radio()':
            radio_player()
        elif inp == 'mute()':
            radio(None, stop=True)
        elif inp == 'myip()':
            show_my_ip()
        elif inp in ('v', 'version()'):
            version()
        elif inp == 'commands()':
            show_commands()
        elif inp == 'add()':
            add_item()
            read_json()
        elif inp == 'hits()':
            SearchHits.show_tag_list()
        elif inp.startswith("pymotw:"):
            site = "pymotw.com"
            cmd_go1(inp[inp.find(':')+1:], site=site)
        elif inp.startswith("go:"):
            cmd_google(inp[inp.find(':')+1:])
        elif inp.startswith("go1:"):
            cmd_go1(inp[inp.find(':')+1:])
        elif inp.startswith("imdb:"):
            site = "imdb.com"
            cmd_go1(inp[inp.find(':')+1:], site=site)
        elif inp.startswith("amazon:"):
            site = "amazon.com"
            cmd_go1(inp[inp.find(':')+1:], site=site)
        elif inp.startswith("youtube:"):
            cmd_youtube(inp[inp.find(':')+1:])
        elif inp.startswith("wp:"):
            site = "wikipedia.org"
            cmd_go1(inp[inp.find(':')+1:], site=site)
        elif inp.startswith("lib:"):
            site = "docs.python.org/2/library/"
            cmd_go1(inp[inp.find(':')+1:], site=site)
        elif inp.startswith("lib3:"):
            site = "docs.python.org/3/library/"
            cmd_go1(inp[inp.find(':')+1:], site=site)
        elif inp.startswith("shorten:"):
            shorten_url(inp[inp.find(':')+1:])
        # disabled, always show the search hits
        #elif inp in tag2keys:
        #    tag = inp
        #    command(tag)
        elif re.search(r'^\d+$', inp):
            try:
                index = int(inp)-1
                if index < 0:
                    raise IndexError
                tag = SearchHits.hits[index].tag
                command(tag)
            except IndexError:
                print "out of range..."
        elif re.search(r'^\d+\.(doc|action|tags|json|url|link|key|jet|edit)(\(\))?$', inp):
            try:
                pos = inp.find('.')
                index = int(inp[:pos])-1
                what = inp[pos+1:].rstrip("()")
                if index < 0:
                    raise IndexError
                hit = SearchHits.hits[index]
                hit.inspect(what)
            except IndexError:
                print "out of range..."
        elif re.search(r'^this.(doc|action|tags|json|url|link|key|jet|edit)(\(\))?$', inp):
            try:
                if not last_key:
                    raise NoLastKeyError
                pos = inp.find('.')
                what = inp[pos+1:].rstrip("()")
                hit = Hit(tag=None, key=last_key)
                hit.inspect(what)
            except NoLastKeyError:
                pass
        elif inp == 'pid()':
            pid_alert()
        elif inp == 'debug()':
            debug()
        else:
            if len(inp) == 1:
                print "too short..."
            else:
                SearchHits.show_hint(inp)


# -------------------------------------

autocomplete_commands += [
    'debug()',    # for development only
    'light()', 'dark()',
    'help()',
    'tags()', 'all()',
    'last()',
    'doc()',
    'edit()',
    'gedit()',
    'less()',
    'bash', 'python',    # to be used as !bash and !python
    'urls()', 'links()',
    'cb()', 'tocb()',
    'json.reload()', 'json.view()', 'json.edit()', 'jet()',
    'this.doc', 'this.action', 'this.tags', 'this.json', 'this.url', 'this.link', 'this.key', 'this.jet()', 'this.edit()',
    'hits()',
    'reddit()',
    'radio()', 'mute()',
    'myip()',
    'commands()',
    'add()',
    'clear()',
    'quit()', 'exit()',
    'version()',
    'doc', 'action', 'tags', 'json', 'url', 'link', 'key',
    'pid()',
]

def info():
    # If you add something to it, add it to the
    # global autocomplete_commands list too!
    text = """
h               - this help (or: help())
t, d            - available tags (or: tags(), all())
p               - python shell
<key>           - call the action that is associated to <key>
<number>        - select a key from the previously shown list of keys
last()          - show last key (debug)
doc()           - show the doc of the last item
!!              - call last command
!cmd            - execute shell command (ex.: !date)
edit()          - edit the file last shown
gedit()         - open the file last shown with gedit
less()          - open the file last shown with less
urls()          - show URLs in the file last shown
tocb()          - copy the output of the last command to the clipboards (or: cb())
json
  .reload()     - reload the json "database"
  .view()       - view the json "database"
  .edit()       - edit the json "database"
  .edit(this)   - edit the json entry of the last selection (or: jet())
NUM         - where NUM is the number of a tag in the search list
  .doc, .action, .tags, .key, .json, .url, .link, .jet, .edit
this
  .doc, .action, .tags, .json, .url, .link, .key, .jet, .edit
hits()          - latest search hits
reddit()        - reddit...
radio()         - radio player...
mute()          - stop radio player
myip()          - my public IP address
v               - version (or: version())
commands()      - list available commands (a command has the form cmd:param)
add()           - add new item
pid()           - pid alert...
light(), dark() - adjust colors to background
c               - clear screen (or: clear())
q               - quit (or: qq, qq(), quit(), exit())
"""
    print text.strip()

# -------------------------------------

autocomplete_commands += [
    'pymotw:',
    'go:',
    'go1:',
    'imdb:',
    'youtube:',
    'amazon:',
    'wp:',
    'lib:',
    'lib3:',
    'shorten:',
]

def show_commands():
    # If you add something to it, add it to the
    # global autocomplete_commands list too!
    text = """
Available commands:
-------------------
pymotw:     - open on PyMOTW, e.g. pymotw:atexit
go:         - Google search list
go1:        - open first google hit
imdb:       - open on IMDb
youtube:    - open on YouTube
wp:         - open on wikipedia
lib:        - look up in Python 2 Standard Library
lib3:       - look up in Python 3 Standard Library
shorten:    - shorten URL
"""
    print text.strip()

# -------------------------------------

def my_exit(error_code=0):
    # threads are subscribed to this signal
    exit_signal.send()
    #
    sys.exit(error_code)


def cleanup():
    exit_signal.send()


def main():
    atexit.register(cleanup)
    check_dependencies()
    setup_history_and_tab_completion()
    #
    read_json(verbose=False)
    header()
    menu()

#############################################################################

if __name__ == "__main__":
    main()
