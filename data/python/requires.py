import os
import sys
# related tag: which

def requires(fpath):
    """
    Verify if the given external command is available.

    Useful when writing "shell scripts" and you want to make
    an external call. If the command (parameter fpath) to be
    called is not available, you get an error message right away.
    """
    def _decorator(fn):
        if not fs.which(fpath):
            print "Error: {f} doesn't exist".format(f=fpath)
            print "Traceback: {func}() in {src}".format(func=fn.__name__, src=__file__)
            sys.exit(1)
        #
        def step_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return step_func
    return _decorator


@requires('mplayer')
def play(movie):
    os.system("mplayer " + movie)
