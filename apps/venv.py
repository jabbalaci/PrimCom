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

from lib import common
from unipath import Path

DONE = True


def get_python_ver():
    """
    Get Python version from the user: 2 or 3.

    The selected Python interpreter will be used in the created virt. env.
    """
    while True:
        try:
            inp = raw_input("~~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        if len(inp) == 0:
            continue
        elif inp == 'q':
            return
        elif inp == 'qq':
            common.my_exit(0)
        elif inp == '2':
            print("with Python 2")
            return 2
        elif inp == '3':
            print("with Python 3")
            return 3
        else:
            print("Hm?")


def mk_virtualenvwrapper():
    """
    Create the virt. env. with virtualenvwrapper.
    """
    print("""
mkvirtualenvwrapper
[2] with Python 2
[3] with Python 3
--------
[q] <<
    """.strip())
    python_ver = get_python_ver()
    if python_ver not in (2, 3):
        return
    #
    venv_name = os.path.split(os.getcwd())[1]
    inp = raw_input("Name of virt. env. (default: {}): ".format(venv_name))
    if len(inp) == 0:
        inp = venv_name
    venv_name = inp
    venv_dir = "{home}/.virtualenvs/{name}".format(home=os.path.expanduser("~"), name=venv_name)
    if python_ver == 2:
        cmd = "source `which virtualenvwrapper.sh` && mkvirtualenv -p `which python2` {name}".format(name=venv_name)
    else:  # Python 3.4+
        cmd = "pyvenv {venv_dir}".format(venv_dir=venv_dir)
    print("#", cmd)
    inp = raw_input("Execute the command above (Y/n)? ").lower()
    if inp in ('', 'y'):
        os.system(cmd)
        with open(".venv", "w") as f:
            print(venv_dir, file=f)
            print("# .venv is created too")
        with open(Path(venv_dir, ".project"), "w") as f:
            print(os.getcwd(), file=f)
            print("# $VENV/.project is created too")
    else:
        print('no.')

    return DONE


def mk_virtualenv():
    """
    Create the virt. env. with virtualenv.
    """
    print("""
mkvirtualenv
[2] with Python 2
[3] with Python 3
--------
[q] <<
    """.strip())
    python_ver = get_python_ver()
    if python_ver not in (2, 3):
        return
    #
    venv_name = raw_input("Name of virt. env. (default: venv): ")
    if len(venv_name) == 0:
        venv_name = "venv"
    cmd = "virtualenv -p python{v} {name}".format(v=python_ver, name=venv_name)
    print("#", cmd)
    inp = raw_input("Execute the command above (y/n, default: y)? ")
    if inp in ('', 'y'):
        os.system(cmd)
        with open(".venv", "w") as f:
            print(venv_name, file=f)
            print("# .venv is created too")
            return DONE
    else:
        print('no.')


def start():
    """
    Create a virtual environment.
    """
    print("""
[1] with virtualenvwrapper / pyvenv
[2] with virtualenv
--------
[q] <<
    """.strip())
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        if len(inp) == 0:
            continue
        elif inp == 'q':
            return
        elif inp == 'qq':
            common.my_exit(0)
        elif inp == '1':
            if mk_virtualenvwrapper() is DONE:
                return DONE
        elif inp == '2':
            if mk_virtualenv() is DONE:
                return DONE
        else:
            print("Hm?")

##############################################################################

if __name__ == "__main__":
    start()
