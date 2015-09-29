#!/usr/bin/env bash

# which Python version to use in the created virt. env. (2 or 3)
PYTHON_VER=2

ppwd=`which pwd`
cd `$ppwd`
a=`pwd`
f=${a##*/}
source `which virtualenvwrapper.sh` && mkvirtualenv -p `which python${PYTHON_VER}` $f
