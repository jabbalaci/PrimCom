import Queue

q = Queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print q.get()    # 0 1 2 3 4

## or: ##################

>>> from collections import deque
>>>
>>> q = deque()
>>> q.append(1); q.append(3); q.append(5)    # q = deque([1,3,5])
>>> q
deque([1, 3, 5])
>>> q.popleft()
1
>>> q
deque([3, 5])
