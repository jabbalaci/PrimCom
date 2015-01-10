from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import requests

from lib.clipboard import text_to_clipboards


def show_my_ip():
    r = requests.get("http://jsonip.com/")
    ip = r.json()["ip"]
    print(ip)
    text_to_clipboards(ip)
