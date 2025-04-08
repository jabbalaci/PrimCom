#!/usr/bin/env python

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

import os
import random


def my_hash(bits=96):
    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
    if len(s) < required_length:
        return my_hash(bits)
    else:
        return s


def create_temp_folder():
    """
    Create a temporary folder with an informative suffix.

    I use this function when I want to share something with
    my friends over Dropbox. In Dropbox/Public I can create a
    temporary folder with an informative suffix so I will know
    by the name of the folder what is in it. These folders are
    usually removed in a few days.
    """
    prefix = my_hash()
    try:
        suffix = input("Informative suffix [optional]: ")
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if suffix:
        suffix = "-" + suffix
    length = 6
    while True:
        dname = "{0}{1}".format(prefix[:length], suffix)
        if not os.path.exists(dname):
            break
        length += 1
        if length > 256:
            break # it's not likely that we get here...
    if not os.path.exists(dname):
        os.mkdir(dname)
        print("# folder created:", os.path.abspath(dname))
    else:
        # it's not likely that we get here...
        print("Warning! The file/folder {} already exists.".format(os.path.abspath(dname)))

##############################################################################

if __name__ == "__main__":
    create_temp_folder()
