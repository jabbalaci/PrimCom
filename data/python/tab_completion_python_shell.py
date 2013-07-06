# ~/.bashrc
export PYTHONSTARTUP=$HOME/.pythonstartup.py

# ~/.pythonstartup.py
try:
    import readline
    import rlcompleter
    import atexit
    import os
except ImportError:
    print "Python shell enhancement modules not available."
else:
    histfile = os.path.join(os.environ["HOME"], ".pythonhistory")
    readline.parse_and_bind("tab: complete")
    if os.path.isfile(histfile):
        readline.read_history_file(histfile)
    atexit.register(readline.write_history_file, histfile)
    del os, histfile, readline, atexit
    print "Python shell history and tab completion are enabled."

# source: http://jbisbee.blogspot.hu/2013/07/add-history-and-tab-completion-to.html
