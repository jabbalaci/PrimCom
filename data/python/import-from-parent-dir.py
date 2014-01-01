
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

def load_src(rel_path, name=None):
    import os, imp
    if name is None:
        name = os.path.splitext(os.path.split(rel_path)[1])[0]
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), rel_path))

eh = load_src("../helper/eh.py")    # equivalent to "import eh"
gotcha = load_src("./gotcha.py")    # equivalent to "import gotcha"

from gotcha import semmi
print eh.SOMETHING
