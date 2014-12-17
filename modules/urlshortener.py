#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

import requests
from termcolor import colored

import config as cfg
from lib.clipboard import text_to_clipboards
from lib.common import cindex
from lib.pyshorteners import shorteners
from lib.pyshorteners.exceptions import ShorteningErrorException
from lib.pyshorteners.utils import is_valid_url


class InvalidUrlException(Exception):
    pass


def bold(text, color='white'):
    return colored(text, color, attrs=['bold'])

#import json
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

def simplify_url(url):
    return url.strip().rstrip("/")


def show_short_url(short_url, long_url=None, expanded=None):
    print(cindex(short_url, color=cfg.colors[cfg.g.BACKGROUND]["cindex"]))
    if long_url and expanded:
        expanded = simplify_url(expanded)
        if expanded == long_url:
            feedback = cindex("(match)", color="green")
        else:
            feedback = cindex("(differs)", color="red")
        print('# expanded from shortened URL: {url} {f}'.format(url=expanded, f=feedback))
    text_to_clipboards(short_url)
    print("# use show() to zoom in")


def shorten_url(long_url):
    long_url = simplify_url(long_url)
    classes = [shorteners.GoogleShortener,
               shorteners.TinyurlShortener,
               shorteners.IsgdShortener]
    for cl in classes:
        try:
            if not is_valid_url(long_url):
                raise InvalidUrlException
            obj = cl()
            short_url = obj.short(long_url)
            expanded = obj.expand(short_url)
            show_short_url(short_url, long_url, expanded)
            break
        except InvalidUrlException:
            print("Error: invalid URL.")
            break
        except ShorteningErrorException as e:
            print('# {cl}: {err}.'.format(cl=obj.__class__.__name__, err=e))
        except requests.exceptions.MissingSchema as e:
            print('# error:', e)
            break

##############################################################################

if __name__ == "__main__":
    url = raw_input("Long URL: ")
    shorten_url(url)
