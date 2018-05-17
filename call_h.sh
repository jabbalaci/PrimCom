#!/usr/bin/env bash

source /home/jabba/.virtualenvs/PrimCom_project-*/bin/activate

cd /home/jabba/Dropbox/python/PrimCom_project
./h.py "$@"

deactivate
