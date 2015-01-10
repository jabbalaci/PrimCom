from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from config import ROOT
from lib.common import my_exit, open_url


def read_subreddits():
    with open("{root}/modules/assets/reddit.txt".format(root=ROOT)) as f:
        return [line for line in [line.rstrip("\n") for line in f.readlines()] \
                if len(line) > 0 and not line.startswith("#")]


def enter_subreddit():
    try:
        sr = raw_input("subreddit: ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return None
    #
    if len(sr) > 0:
        open_subreddit(sr)
        return True
    #
    return None


def open_subreddit(sr):
    url = "http://www.reddit.com/r/{sr}".format(sr=sr)
    open_url(url)


def reddit():
    li = read_subreddits()
    #
    for index, subreddit in enumerate(li, start=1):
        print("[{i}] {sr}".format(i=index, sr=subreddit))
    print("[s] specify subreddit (without /r/)")
    print("[q] <<")
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if len(inp) == 0:
            continue
        elif inp == 's':
            ok = enter_subreddit()
            if ok:
                return
        elif inp == 'q':
            return None
        elif inp == 'qq':
            my_exit(0)
        else:
            try:
                index = int(inp) - 1
                if index < 0:
                    raise IndexError
                open_subreddit(li[index])
                return
            except IndexError:
                print("out of range...")
            except ValueError:
                print('Wat?')
