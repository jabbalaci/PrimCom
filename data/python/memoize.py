"""
from http://www.reddit.com/r/Python/comments/20x61y/share_the_code_youre_most_proud_of/

Note: "Just be careful of memory leaks, as the cache will never be cleared for
the lifetime of the program."
"""

# Python 2:
def memoize(f):
    """
    Memoization decorator.

    >>> @memoize
    ... def fib(n):
    ...     return 1 if n < 2 else fib(n-1) + fib(n-2)
    ...
    >>> fib(100)
    573147844013817084101

    """
    cache = {}
    def helper(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return helper

########################################

"""
Python 3
http://docs.python.org/3/library/functools.html#functools.lru_cache

Decorator to wrap a function with a memoizing callable...
It can save time when an expensive or I/O bound function is
periodically called with the same arguments.
"""
import functools
@functools.lru_cache(None)
def fib(n):
    return 1 if n < 2 else fib(n-1) + fib(n-2)
