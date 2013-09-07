# Python 3.4
from contextlib import ignored

with ignored(OSError):
    os.unlink('somefile.txt')

####################

# Python 2.7
from contextlib import contextmanager
 
@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass

with ignored(OSError):
    os.unlink('somefile.txt')

# by Raymond Hettinger
# http://www.youtube.com/watch?v=OSGv2VnC0go , relevant part at 43:30
