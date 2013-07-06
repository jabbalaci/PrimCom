import os

my_file = '/home/jabba/python/filepath/hello.py'

dname, fname = os.path.split(my_file)
print dname    # /home/jabba/python/filepath
print fname    # hello.py

base_name, ext = os.path.splitext(fname)
print base_name    # hello
print ext          # .py
