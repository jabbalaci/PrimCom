
import os
import sys

# import from parent directory, i.e.
# add the path of the parent directory to sys.path
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ~~~~~~~~~~~~~~~~~~~~

import sys
# to be able to import something from the lib (if normal import didn't work)
sys.path.insert(0, "./lib/")

# ~~~~~~~~~~~~~~~~~~~~

def load_src(name, fpath):
    import os, imp
    p = fpath if os.path.isabs(fpath) \
        else os.path.join(os.path.dirname(__file__), fpath)
    return imp.load_source(name, p)

load_src("eh", "../helper/eh.py")
import eh
load_src("gotcha", "./gotcha.py")
from gotcha import nothing

print eh.SOMETHING
print nothing()
