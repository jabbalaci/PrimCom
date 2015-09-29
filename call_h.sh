#!/usr/bin/env bash

source ~/.virtualenvs/PrimCom_project/bin/activate

cd ~/Dropbox/python/PrimCom_project
./h.py "$@"

deactivate
