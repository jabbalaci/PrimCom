import os
import sys

for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        fname = os.path.join(root, f)
        print fname
        # Remove *.pyc files, compress images, count lines of code
        # calculate folder size, check for repeated files, etc.
        # A lot of nice things can be done here
        # credits: m_tayseer @reddit
