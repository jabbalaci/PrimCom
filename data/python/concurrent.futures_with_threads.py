#!/usr/bin/env python

from Queue import Queue
import concurrent.futures
import random
import time

q = Queue()
fred = [1,2,3,4,5,6,7,8,9,10]


def f(x):
    if random.randint(0,1):
        time.sleep(0.1)
    #
    res = x * x
    q.put(res)


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for num in fred:
            executor.submit(f, num)
    #
    while not q.empty():
        print q.get()


if __name__ == "__main__":
    main()

