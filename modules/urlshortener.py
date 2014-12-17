#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

from termcolor import colored

import config as cfg
from lib.clipboard import text_to_clipboards
from lib.common import cindex
from lib.pyshorteners import shorteners
from lib.pyshorteners.exceptions import ShorteningErrorException


def bold(text, color='white'):
    return colored(text, color, attrs=['bold'])

#import json
#import requests
#
#def shorten_url(long_url):
#    try:
#        url = "https://www.googleapis.com/urlshortener/v1/url"
#        data = {"longUrl": long_url}
#        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#        r = requests.post(url, data=json.dumps(data), headers=headers)
#        short = r.json()["id"]
##        print(short)
#        print(cindex(short, color=cfg.colors[cfg.g.BACKGROUND]["cindex"]))
#        text_to_clipboards(short)
#        print("# use show() to zoom in")
#    except:
#        print("Hmm, strange...")

def show_short_url(short_url):
    print(cindex(short_url, color=cfg.colors[cfg.g.BACKGROUND]["cindex"]))
    text_to_clipboards(short_url)
    print("# use show() to zoom in")


def shorten_url(long_url):
    classes = [shorteners.GoogleShortener,
               shorteners.TinyurlShortener,
               shorteners.IsgdShortener]
    for cl in classes:
        try:
            obj = cl()
            short_url = obj.short(long_url)
        except ShorteningErrorException as e:
            print('# {cl}: {err}.'.format(cl=obj.__class__.__name__, err=e))
        else:
            show_short_url(short_url)
            print('# expanded from shortened URL:', obj.expand(short_url))
            break

##############################################################################

if __name__ == "__main__":
    url = raw_input("Long URL: ")
    shorten_url(url)
