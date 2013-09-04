import Queue

q = Queue.LifoQueue()

for i in range(5):
    q.put(i)

while not q.empty():
    print q.get()    # 4 3 2 1 0

## or: ##################

>>> li
[1, 4, 6]
>>> li.append(8)
>>> li
[1, 4, 6, 8]
>>> while li:
...     print li.pop()
... 
8
6
4
1
