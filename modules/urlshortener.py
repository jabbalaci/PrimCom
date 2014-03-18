#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

import json

import requests
from termcolor import colored

from lib.clipboard import text_to_clipboards


def bold(text, color='white'):
    return colored(text, color, attrs=['bold'])


def shorten_url(long_url):
    try:
        url = "https://www.googleapis.com/urlshortener/v1/url"
        data = {"longUrl": long_url}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        short = r.json()["id"]
        print(short)
        text_to_clipboards(short)
        print(bold("# use show() to zoom in"))
    except:
        print("Hmm, strange...")

##############################################################################

if __name__ == "__main__":
    url = raw_input("Long URL: ")
    shorten_url(url)
