# blog post: http://goo.gl/oEdtT3

# virtualenvwrapper for Python 3 or Python 2
mkvirtualenv -p `which python3` myenv3
mkvirtualenv -p `which python2` myenv2

# virtualenv for Python 3 or Python 2
virtualenv -p python3 myproject3
virtualenv -p python2 myproject2

# When the env. is created, activate it
# and launch the command python within.
# Verify if it's the correct version.
