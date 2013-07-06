
import os
import sys

# import from parent directory
if __name__ == "__main__":
    package_dir = ".."
    package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
    sys.path.insert(0, package_dir_path)

# ~~~~~~~~~~~~~~~~~~~~

import sys
# to be able to import something from the lib (if normal import didn't work)
sys.path.insert(0, "./lib/")
