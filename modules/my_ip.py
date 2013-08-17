import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests
from lib.clipboard import text_to_clipboards


def show_my_ip():
    r = requests.get("http://jsonip.com/")
    ip = r.json()["ip"]
    print ip
    text_to_clipboards(ip)
