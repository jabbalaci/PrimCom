#!/usr/bin/env python

import sys
import redis
import concurrent.futures

r = redis.Redis()
fred = [1,2,3,4,5,6,7,8,9,10]


def check_server():
    try:
        r.info()
    except redis.exceptions.ConnectionError:
        print >>sys.stderr, "Error: cannot connect to redis server. Is the server running?"
        sys.exit(1)


def f(x):
    res = x * x
    r.rpush("test", res)


def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for num in fred:
            executor.submit(f, num)
    #
    print r.lrange("test", 0, -1)

####################

if __name__ == "__main__":
    check_server()
    ###
    r.delete("test")
    main()

