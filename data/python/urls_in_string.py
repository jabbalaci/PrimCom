# http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python

import re

def extract_urls(fname):
    with open(fname) as f:
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())
