import os
import sys

for path, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        fullname = os.path.join(path, f)
        print fullname
        # Remove *.pyc files, compress images, count lines of code
        # calculate folder size, check for repeated files, etc.
        # A lot of nice things can be done here
        # credits: m_tayseer @reddit
