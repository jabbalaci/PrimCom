import os
from urlparse import urlparse

url = "http://fc00.deviantart.net/fs70/i/2013/050/f/4/hiro_protagonist__snow_crash_by_ariokh-d5vkofi.jpg"
fname = os.path.split(urlparse(url)[2])[1]
print fname    # hiro_protagonist__snow_crash_by_ariokh-d5vkofi.jpg

base_name, ext = os.path.splitext(fname)
print base_name    # hiro_protagonist__snow_crash_by_ariokh-d5vkofi
print ext          # .jpg
