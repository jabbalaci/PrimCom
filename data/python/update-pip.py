#!/usr/bin/env python

"""
Global version. It updates packages that were installed with "sudo".
"""
import os
import pip

dists = []
for dist in pip.get_installed_distributions():
    dists.append(dist.project_name)

for dist_name in sorted(dists, key=lambda s: s.lower()):
    cmd = "sudo pip install {0} -U".format(dist_name)
    print '#', cmd
    os.system(cmd)

########################################

"""
local version, can be used in a virtualenv for instance
"""
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
