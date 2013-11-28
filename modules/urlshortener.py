#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests
from lib.clipboard import text_to_clipboards
import json

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


#def shorten_url(long_url):
#    try:
#        url = "http://gg.gg/?action=create&url=" + long_url
#        r = requests.get(url)
#        short = r.text
#        print short
#        text_to_clipboards(short)
#    except:
#        print "Hmm, strange..."


if __name__ == "__main__":
    url = raw_input("Long URL: ")
    shorten_url(url)
