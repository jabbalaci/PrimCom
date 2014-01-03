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
