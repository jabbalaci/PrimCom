#!/usr/bin/env python

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

from lib.clipboard import text_to_clipboards


def start(url=None):
    """
    Install a Python package directly from GitHub.
    """
    if not url:
        try:
            url = raw_input("GitHub URL of the project: ")
        except (KeyboardInterrupt, EOFError):
            print()
            return

    project_name = url[url.rfind('/')+1:]
    cmd = 'pip install -e git+{url}.git#egg={pn}'.format(url=url, pn=project_name)
    print(cmd)
    text_to_clipboards(cmd)

##############################################################################

if __name__ == "__main__":
    start("https://github.com/morninj/django-email-obfuscator")
