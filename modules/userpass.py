#!/usr/bin/env python

"""
Username and password generator.

Made for online registrations.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

import string
from random import choice, randint, shuffle

from lib import markov_passwords
from lib.common import my_shuffle


def get_username(length=6):
    """
    Returns a readable (Japanese-style) username.
    """
    return markov_passwords.get_word(length)


def get_password(length=8):
    """
    Create a password with uppercase letters, lowercase letters, and digits.

    The password will include lowercase letters with higher probability.
    """
    assert length >= 8
    #
    chars = string.ascii_lowercase + string.ascii_lowercase + string.ascii_lowercase + \
            string.ascii_uppercase + string.digits + string.digits + string.digits
    chars = ''.join(my_shuffle([x for x in chars]))
    return ''.join(choice(chars) for x in range(length))


def get_urandom_password(length=8):
    """
    Get data from /dev/urandom .
    """
    assert length >= 8
    #
    li = []
    with open("/dev/urandom") as f:
        while len(li) < length:
            c = f.read(1)
            if c.isalnum():
                li.append(c)

    return ''.join(li)

#############################################################################

if __name__ == "__main__":
    print(get_username())
    print(get_password(length=12))
    print()
    print(get_urandom_password(length=12))
