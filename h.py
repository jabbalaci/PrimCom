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

import time

start_time = time.time()

import atexit
import json
import os
import re
import readline
import sys
from collections import OrderedDict
from threading import Thread
from urllib.parse import urljoin

import requests

import apps
import config as cfg
from lib import clipboard, common, fs
from lib.clipboard import text_to_clipboards
from lib.common import bold, cindex, exit_signal, my_exit, open_url, requires
from modules import (
    colored_line_numbers,
    conferences,
    header,
    my_ip,
    pidcheck,
    reddit,
    selected_lines,
    show,
    urlshortener,
    userpass,
)

# If you want the command "less" to use colors, follow the steps in this post:
# https://ubuntuincident.wordpress.com/2013/06/05/syntax-highlighted-less-in-command-line/

# these are all re-set in read_json()
hdict = OrderedDict()  # will be set later
tag2keys = OrderedDict()  # will be set later
# search_result = []         # will be updated after each search
last_key = None  # will be updated after each command
autocomplete_commands = []  # will be filled later (used for autocomplete)

dependencies = {
    # command: package installation
    "pygmentize": "sudo apt-get install python-pygments",
    "xsel": "sudo apt-get install xsel",
}

LOAD_JSON = cfg.LOAD_JSON


#############
## Helpers ##
#############


class NoLastKeyError(Exception):
    pass


def check_dependencies():
    for prg in dependencies:
        if not fs.which(prg):
            print("Warning: {0} is not available.".format(prg))
            print("tip: {0}".format(dependencies[prg]))


def completer(text, state):
    # for autocomplete
    if re.search(r"^\d+\.", text):  # if it starts with a number
        pos = text.find(".")
        num = text[:pos]
        text = text[pos + 1 :]
        options = [x for x in autocomplete_commands if x.startswith(text)]
        try:
            return num + "." + options[state]
        except IndexError:
            return None
    else:  # normal case
        options = [x for x in autocomplete_commands if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None


def truncate_histfile(hfile):
    """
    Leave the last N lines of histfile.
    """
    hfile_bak = hfile + ".bak"
    if os.path.isfile(hfile):
        os.system(
            "tail -{N} {hf} >{hf_bak}".format(
                N=cfg.TRUNCATE_HISTFILE_TO_LINES, hf=hfile, hf_bak=hfile_bak
            )
        )
        if os.path.isfile(hfile_bak):
            os.unlink(hfile)
            os.rename(hfile_bak, hfile)


def setup_history_and_tab_completion():
    histfile = "{root}/.history".format(root=cfg.ROOT)
    #
    truncate_histfile(histfile)
    #
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
        return val[: val.find("/")]
    elif action[0] == "open_url":
        return "urls"
    #
    return None


def fname_to_abs(fname):
    """
    In the json files, file names are given like this: "flask/hello.py".
    Let's convert it to absolute path.
    """
    return "{root}/data/{f}".format(root=cfg.ROOT, f=fname)


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
        for o in hdict.values():
            for t in o["tags"]:
                if inp in t.lower():
                    # li.append(t)
                    SearchHits.add(t)
        #
        SearchHits.remove_duplicates_and_keep_order()
        #
        # if li:
        if SearchHits.hits:
            # show_tag_list(li)
            SearchHits.show_tag_list()
        else:
            print("Wat?")

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
            sys.stdout.write(e.to_str(index))
            sys.stdout.write(" ")
        print()


##########


class Hit(object):
    def __init__(self, tag, key=None):
        if not key:  # normal "constructor":
            self.tag = tag
            self.keys = tag2keys[tag]
            if len(self.keys) == 1:
                self.o = hdict[self.keys[0]]
            else:
                self.o = None
        else:  # alternative "constructor":
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
            if what in ("doc", "action", "tags"):
                print(o[what])
            elif what == "json":
                print(json.dumps(o, indent=4))
            elif what in ("url", "link"):
                if self.is_link():
                    print(o["action"][1])
            elif what == "key":
                print(self.keys[0])
            elif what == "edit":
                if len(self.keys) == 1:
                    edit(self.keys[0])
            elif what == "jet":
                if len(self.keys) == 1:
                    edit_entry(self.keys[0])
            else:
                print("Wat?")

    def to_str(self, index):
        s = ""
        if self.is_link():
            s += cindex("({0}) ".format(index), color=cfg.colors[cfg.g.BACKGROUND]["cindex_link"])
        else:
            s += cindex("({0}) ".format(index))
        s += self.tag
        if len(self.keys) > 1:
            s += "..."
        return s


##########
## Core ##
##########


def process(d):
    t2k = OrderedDict()  # tag2keys
    #
    for k in d.keys():
        o = d[k]
        if not (("doc" in o) and ("action" in o) and ("tags" in o)):
            print("Error: '{k}' must have doc, action, and tags.".format(k=k))
            my_exit(1)
        if len(o["doc"]) == 0:
            print("Error: '{k}' must have a valid doc.".format(k=k))
            my_exit(1)
        if len(o["tags"]) == 0:
            print("Error: '{k}' must have at least one tag.".format(k=k))
            my_exit(1)
        for t in o["tags"]:
            t = t.strip()
            if t[0] == "_":
                print("Error: the tag {tag} cannot start with an underscore.".format(tag=t))
                my_exit(1)
            if len(t) == 1:
                print("Error: the tag '{t}' in {k} is too short.".format(t=t, k=k))
                my_exit(1)
            if t in t2k:
                t2k[t].append(k)
            else:
                t2k[t] = [k]
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
        with open(fname_to_abs(db)) as f:
            tmp = json.load(f, object_pairs_hook=OrderedDict)
        for k in tmp:
            hdict[k] = tmp[k]
        if verbose:
            print("# {db} reloaded".format(db=db))
    #
    # sort hdict items by date
    hdict = OrderedDict(sorted(hdict.items(), key=lambda x: x[1]["meta"]["date"]))
    #
    tag2keys = process(hdict)


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
            print("Warning: unknown extra option: {e}".format(e=e))


def extract_urls(fname):
    with open(fname) as f:
        return re.findall(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            f.read(),
        )


def show_urls(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == "cat":
        fname = fname_to_abs(action[1])
    else:
        return

    # OK, we have the fname
    li = extract_urls(fname)
    for index, url in enumerate(li, start=1):
        print("[{i}] {url}".format(i=index, url=url))
    print("[q] <<")
    while True:
        try:
            inp = input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if len(inp) == 0:
            continue
        if inp == "q":
            return None
        if inp == "qq":
            my_exit(0)
        try:
            index = int(inp) - 1
            if index < 0:
                raise IndexError
            open_url(li[index])
            return
        except IndexError:
            print("out of range...")
        except ValueError:
            print("Wat?")


def subcommand(li):
    def is_link(k):
        return Hit(tag=None, key=k).is_link()

    for index, k in enumerate(li, start=1):
        if is_link(k):
            pre = cindex("[{0}]".format(index), color=cfg.colors[cfg.g.BACKGROUND]["cindex_link"])
        else:
            pre = cindex("[{0}]".format(index))
        print(
            "{pre} {main_tag} ({doc})".format(
                pre=pre, main_tag=hdict[k]["tags"][0], doc=hdict[k]["doc"]
            )
        )
    print("[q] <<")
    while True:
        try:
            inp = input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if len(inp) == 0:
            continue
        if inp == "q":
            return None
        if inp == "qq":
            my_exit(0)
        try:
            index = int(inp) - 1
            if index < 0:
                raise IndexError
            perform_action(li[index])
            return
        except IndexError:
            print("out of range...")
        except ValueError:
            print("Wat?")


def debug(text):
    """
    for development
    """
    print(os.getcwd())


def command(inp):
    li = tag2keys[inp]
    if len(li) > 1:
        subcommand(li)
    else:
        perform_action(li[0])


def perform_action(key, search_term=""):
    global last_key
    last_key = key
    #
    o = hdict[key]
    action = o["action"]
    verb = action[0]
    if verb == "cat":
        fname = fname_to_abs(action[1])
        colored_line_numbers.cat(fname, o, search_term)
        process_extras(fname, o)
    elif verb == "open_url":
        open_url(action[1], o["doc"])
    else:
        print("Error: unknown action: {a}.".format(a=verb))
        my_exit(1)


def view_edit_json(key):
    db = get_db_by_key(key)
    os.system(
        "{ed} {f}".format(ed=cfg.EDITOR, f="{root}/data/{db}.json".format(root=cfg.ROOT, db=db))
    )


def to_clipboards(key):
    if fs.which("xsel"):
        o = hdict[key]
        #
        action = o["action"]
        verb = action[0]
        if verb == "cat":
            with open(fname_to_abs(action[1])) as f:
                text_to_clipboards(f.read().rstrip("\n"))
    else:
        print("Warning: xsel is not installed, cannot copy to clipboards.")


def path_to_clipboards(key):
    if fs.which("xsel"):
        o = hdict[key]
        #
        action = o["action"]
        verb = action[0]
        if verb == "cat":
            f = fname_to_abs(action[1])
            print("#", f)
            text_to_clipboards(f)
    else:
        print("Warning: xsel is not installed, cannot copy to clipboards.")


def key_to_file(key):
    """
    We have a key and figure out its corresponding file.

    It only makes sense if the action is "cat".
    """
    if key is None:
        return None
    #
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == "cat":
        f = fname_to_abs(action[1])
        return f
    # else, if it's a URL to open
    return None


def show_doc(key):
    o = hdict[key]
    print(o["doc"])


@requires(cfg.EDITOR)
def edit(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == "cat":
        os.system("{ed} {fname}".format(ed=cfg.EDITOR, fname=fname_to_abs(action[1])))


@requires(cfg.GEDIT)
def gedit(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == "cat":
        os.system("{ed} {fname} &".format(ed=cfg.GEDIT, fname=fname_to_abs(action[1])))


def less(key):
    o = hdict[key]
    #
    action = o["action"]
    verb = action[0]
    if verb == "cat":
        os.system("less {fname}".format(fname=fname_to_abs(action[1])))


def first_google_hit(keyword):
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + keyword
    r = requests.get(url)
    d = r.json()
    return d["responseData"]["results"][0]["url"]


def cmd_google(keyword):
    open_url("https://www.google.com/search?q=" + keyword)


def cmd_def(word):
    keyword = "{w} meaning".format(w=word)
    cmd_google(keyword)


def cmd_youtube(keyword):
    open_url("https://www.youtube.com/results?search_query=" + keyword)


def cmd_go1(keyword, site=None):
    if not site:
        q = keyword
    else:
        q = "site:{site} {kw}".format(site=site, kw=keyword)
    #
    url = first_google_hit(q)
    open_url(url)


def open_pep(num):
    url = "http://www.python.org/dev/peps"
    if num:
        url = "{url}/pep-{num}".format(url=url, num=num.zfill(4))
    #
    open_url(url)


def toggle_line_numbers():
    cfg.SHOW_LINE_NUMBERS = not cfg.SHOW_LINE_NUMBERS
    print("show line numbers:", "on" if cfg.SHOW_LINE_NUMBERS else "off")


def add_item():
    os.system("python2 {root}/add_item.py".format(root=cfg.ROOT))


def edit_entry(key):
    db = get_db_by_key(key)
    dbfile = "{root}/data/{db}.json".format(root=cfg.ROOT, db=db)
    d = OrderedDict()
    d[key] = hdict[key]
    tmpfile = "{root}/tmp/temp.{pid}.json".format(root=cfg.ROOT, pid=os.getpid())
    with open(tmpfile, "w") as f:
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
    tmpfile = "{root}/tmp/{db}.json.bak".format(root=cfg.ROOT, db=db)
    os.rename(dbfile, tmpfile)
    assert os.path.isfile(tmpfile)
    with open(dbfile, "w") as f:
        json.dump(dbdict, f, indent=4)
    print("# edited")
    read_json()


def version():
    text = """
PrimCom {v} ({date}) by Laszlo Szathmary (jabba.laci@gmail.com), 2013--2014
""".format(v=cfg.__version__, date=cfg.__date__)
    print(text.strip())


def print_header():
    header.header()


def change_dir(inp):
    bak = os.getcwd()
    #
    if inp == "cd":
        os.chdir(os.path.expanduser("~"))
    elif inp == "cd -":
        os.chdir(change_dir.prev_dir)
    elif inp.startswith("cd "):
        dest = inp.split()[1]
        try:
            os.chdir(dest)
        except OSError:
            print("Warning! No such file or directory")

    #    print(os.getcwd())
    # static variable:
    change_dir.prev_dir = bak


def username_password():
    """
    Generate username and password.

    This is used for online registrations.
    The function has a static variable called
    "password", set in init().
    If you provide your email in the file
    email.txt, you can also copy it to the
    clipboards.
    """
    username = userpass.get_username()
    password = userpass.get_password(length=16)
    try:
        email = open("{root}/email.txt".format(root=cfg.ROOT)).read().strip()
    except IOError:
        email = None

    print(
        """
[1] {u:21} (username, copy to clipboard)
[2] {p:21} (password, copy to clipboard)
[3] {e:21} (email, copy to clipboard)
[q] <<
""".strip().format(u=username, p=password, e=email)
    )
    while True:
        try:
            inp = input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        if len(inp) == 0:
            continue
        elif inp == "q":
            return
        elif inp == "qq":
            common.my_exit(0)
        elif inp == "1":
            text_to_clipboards(username, prefix="username")
        elif inp == "2":
            text_to_clipboards(password, prefix="password")
            username_password.password = password
        elif inp == "3":
            if email:
                text_to_clipboards(email, prefix="email")
            else:
                print("Warning! You have no email specified.")
                print("Tip: create an email.txt file in the PrimCom folder.")
        else:
            print("Wat?")


@exit_signal.connect
def clear_password(sender):
    """
    Password removal.
    """
    if clipboard.read_primary() == username_password.password:
        clipboard.to_primary("")
    if clipboard.read_clipboard() == username_password.password:
        clipboard.to_clipboard("")
    if username_password.password:
        username_password.password = None


@requires(cfg.EDITOR)
def menu():
    print("[{0:.3f}s]".format(time.time() - start_time), end="\n")
    #
    while True:
        try:
            # inp = input(bold('pc> ')).strip()
            inp = input(bold("{prompt}> ".format(prompt=os.getcwd()))).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            my_exit(0)
        if len(inp) == 0:
            continue
        if inp in ("h", "help()"):
            info()
        elif inp in ("q", "qq", ":q", ":x", "quit()", "exit()"):
            my_exit(0)
        elif inp in ("c", "clear()"):
            os.system("clear")
            print_header()
        elif inp in ("light()", "dark()"):
            if inp == "light()":
                cfg.g.BACKGROUND = cfg.LIGHT
            else:
                cfg.g.BACKGROUND = cfg.DARK
        elif inp in ("t", "tags()", "all()", "d"):
            SearchHits.show_tag_list(tag2keys.keys())
        elif inp == "p":
            os.system("python3")  # default
        elif inp == "p2":
            os.system("python2")
        elif inp == "p3":
            os.system("python3")
        elif inp == "bpy":
            os.system("bpython")
        elif inp == "ipy":
            os.system("ipython")
        elif inp == "last()":
            print(last_key)
        elif inp == "!!":
            if last_key:
                perform_action(last_key)
        elif inp.startswith("!"):
            cmd = inp[1:]
            os.system(cmd)
        elif inp == "edit()":
            if last_key:
                edit(last_key)
        elif inp == "gedit()":
            if last_key:
                gedit(last_key)
        elif inp == "less()":
            if last_key:
                less(last_key)
        elif inp in ("urls()", "links()"):
            if last_key:
                show_urls(last_key)
        elif inp in ("cb()", "tocb()"):
            if last_key:
                to_clipboards(last_key)
        elif inp == "path()":
            if last_key:
                path_to_clipboards(last_key)
        elif inp == "doc()":
            if last_key:
                show_doc(last_key)
        elif inp == "json.reload()":
            read_json()
        elif inp in ("json.view()", "json.edit()"):
            if last_key:
                view_edit_json(last_key)
                read_json()
        elif inp in ("json.edit(this)", "jet()"):
            if last_key:
                edit_entry(last_key)
        elif inp == "reddit()":
            reddit.reddit()
        elif inp == "conferences()":
            conferences.conferences()
        elif inp == "mute()":
            apps.radio.radio(None, stop=True)
        elif inp == "myip()":
            my_ip.show_my_ip()
        elif inp in ("v", "version()"):
            version()
        elif inp == "commands()":
            show_commands()
        elif inp == "add()":
            add_item()
            read_json()
        elif inp == "hits()":
            SearchHits.show_tag_list()
        elif inp.startswith("pymotw:"):
            site = "pymotw.com"
            cmd_go1(inp[inp.find(":") + 1 :], site=site)
        elif inp.startswith("go:"):
            cmd_google(inp[inp.find(":") + 1 :])
        elif inp.startswith("go1:"):
            cmd_go1(inp[inp.find(":") + 1 :])
        elif inp.startswith("imdb:"):
            site = "imdb.com"
            cmd_go1(inp[inp.find(":") + 1 :], site=site)
        elif inp.startswith("amazon:"):
            site = "amazon.com"
            cmd_go1(inp[inp.find(":") + 1 :], site=site)
        elif inp.startswith("youtube:"):
            cmd_youtube(inp[inp.find(":") + 1 :])
        elif inp.startswith("wp:"):
            site = "wikipedia.org"
            cmd_go1(inp[inp.find(":") + 1 :], site=site)
        elif inp.startswith("lib:") or inp.startswith("lib2:"):
            site = "docs.python.org/2/library/"
            cmd_go1(inp[inp.find(":") + 1 :], site=site)
        elif inp.startswith("lib3:"):
            site = "docs.python.org/3/library/"
            cmd_go1(inp[inp.find(":") + 1 :], site=site)
        elif inp.startswith("golib:"):
            site = "http://golang.org/pkg/"
            lib = inp[inp.find(":") + 1 :]
            open_url(urljoin(site, lib))
        elif inp.startswith("shorten:"):
            urlshortener.shorten_url(inp[inp.find(":") + 1 :])
        elif inp.startswith("def:"):
            cmd_def(inp[inp.find(":") + 1 :])
        elif inp.startswith("pep:"):
            open_pep(inp[inp.find(":") + 1 :])
        elif inp == "pep()":
            open_pep(None)
        elif inp == "show()":
            show.show()
        elif inp == "numbers()":
            toggle_line_numbers()
        elif re.search(r"^l([\d,-]+)\.(sh|py|py2|py3|cb|cb\(>\))$", inp):
            fname = key_to_file(last_key)
            selected_lines.process_selected_lines(inp, fname)
        elif inp == "cd" or inp.startswith("cd "):
            change_dir(inp)
        elif inp == "pwd()":
            print(os.getcwd())
        elif inp == "userpass()":
            username_password()
        elif inp == "apps()":
            apps.menu.main()
        elif inp == "k":
            os.system("konsole 2>/dev/null &")
        elif inp.startswith("filter:"):
            term = inp[inp.find(":") + 1 :]
            if last_key:
                perform_action(last_key, term)
        elif inp.startswith("app:"):
            val = inp[inp.find(":") + 1 :]
            if not val:
                apps.menu.main()
            else:
                apps.menu.start_app(val)
        # shortcuts
        elif inp == "radio()":
            apps.menu.start_app_by_shortcut("radio")
        # disabled, always show the search hits
        # elif inp in tag2keys:
        #    tag = inp
        #    command(tag)
        elif re.search(r"^\d+$", inp):
            try:
                index = int(inp) - 1
                if index < 0:
                    raise IndexError
                tag = SearchHits.hits[index].tag
                command(tag)
            except IndexError:
                print("out of range...")
        elif re.search(r"^\d+\.(doc|action|tags|json|url|link|key|jet|edit)(\(\))?$", inp):
            try:
                pos = inp.find(".")
                index = int(inp[:pos]) - 1
                what = inp[pos + 1 :].rstrip("()")
                if index < 0:
                    raise IndexError
                hit = SearchHits.hits[index]
                hit.inspect(what)
            except IndexError:
                print("out of range...")
        elif re.search(r"^this.(doc|action|tags|json|url|link|key|jet|edit)(\(\))?$", inp):
            try:
                if not last_key:
                    raise NoLastKeyError
                pos = inp.find(".")
                what = inp[pos + 1 :].rstrip("()")
                hit = Hit(tag=None, key=last_key)
                hit.inspect(what)
            except NoLastKeyError:
                pass
        elif inp == "pid()":
            pidcheck.pid_alert()
        elif inp == "debug()":
            debug(None)
        elif inp == "song()":
            print("Playing:", apps.radio.get_song())
        else:
            if len(inp) == 1:
                print("too short...")
            else:
                inp = inp.lower()
                SearchHits.show_hint(inp)


# -------------------------------------

autocomplete_commands += [
    "debug()",  # for development only
    "light()",
    "dark()",
    "help()",
    "tags()",
    "all()",
    "last()",
    "doc()",
    "edit()",
    "gedit()",
    "less()",
    "bash",
    "python",  # to be used as !bash and !python
    "urls()",
    "links()",
    "cb()",
    "tocb()",
    "path()",
    "json.reload()",
    "json.view()",
    "json.edit()",
    "jet()",
    "this.doc",
    "this.action",
    "this.tags",
    "this.json",
    "this.url",
    "this.link",
    "this.key",
    "this.jet()",
    "this.edit()",
    "hits()",
    "reddit()",
    "radio()",
    "mute()",
    "song()",
    "conferences()",
    "myip()",
    "commands()",
    "add()",
    "clear()",
    "quit()",
    "exit()",
    "version()",
    "doc",
    "action",
    "tags",
    "json",
    "url",
    "link",
    "key",
    "pid()",
    "show()",
    "numbers()",
    "pwd()",
    "userpass()",
    "apps()",
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
path()          - copy the path of the file last shown to the clipboards
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
song()          - title of the current song on radio
show()          - show the content of the clipboard in the browser
conferences()   - Python conferences
mute()          - stop radio player
myip()          - my public IP address
v               - version (or: version())
commands()      - list available commands (a command has the form cmd:param)
add()           - add new item
pid()           - pid alert...
light(), dark() - adjust colors to background
numbers()       - toggle line numbers
cd              - change directory
pwd()           - print working directory
userpass()      - generate user name and password
apps()          - applications
c               - clear screen (or: clear())
q               - quit (or: qq, qq(), quit(), exit())
"""
    print(text.strip())


# -------------------------------------

autocomplete_commands += [
    "pymotw:",
    "go:",
    "go1:",
    "imdb:",
    "youtube:",
    "amazon:",
    "wp:",
    "lib:",
    "lib2:",
    "lib3:",
    "shorten:",
    "filter:",
    "pep:",
    "def:",
    "golib:",
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
lib:        - look up in Python 2 Standard Library (or: lib2:)
lib3:       - look up in Python 3 Standard Library
shorten:    - shorten URL
filter:     - filter lines of a file that contain a search term
pep:        - open PEP, e.g. pep:8
def:        - define a word
golib:      - open on Go standard library
"""
    print(text.strip())


# -------------------------------------


def init():
    """
    Do some initialization.
    """
    if not hasattr(username_password, "password"):
        username_password.password = None


def cleanup():
    # threads are subscribed to this signal
    exit_signal.send()


#    print("cleanup called")


def check_command_line_arguments():
    args = sys.argv[1:]
    for arg in args:
        if arg in ("-c", "--clear"):
            os.system("clear")
        elif arg in ("-k", "--kill"):
            # suicide mode: do the caching and terminate
            print("Waiting for the threads to finish...")
            background_reads(block=True)
            print("Quit.")
            sys.exit(0)
        else:
            print("Error: unknown option: {}".format(arg), file=sys.stderr)
            sys.exit(1)


def background_reads(block=False):
    """
    Start these jobs in the background.

    These things are necessary but they take some seconds to complete.
    Idea: show the prompt right away then finish these things a bit later.
    If block is True (used in suicide mode), then we are waiting here
    until all threads are stopped.
    """
    t1 = Thread(target=check_dependencies)
    t2 = Thread(target=setup_history_and_tab_completion)
    t3 = Thread(target=read_json, kwargs={"verbose": False})
    t4 = Thread(target=colored_line_numbers.cache_pygmentize)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    if block:
        t1.join()
        t2.join()
        t3.join()
        t4.join()


def main():
    background_reads()
    #
    print_header()
    menu()


#############################################################################

if __name__ == "__main__":
    init()
    atexit.register(cleanup)
    check_command_line_arguments()
    main()
