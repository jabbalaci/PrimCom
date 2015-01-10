from collections import defaultdict

def default_factory():
    return 'default value'

d = defaultdict(default_factory)
d["foo"] = "bar"
print d["foo"]    # bar
print d["bar"]    # default value

##########

s = 'mississippi'
d = defaultdict(int)    # because int() returns 0
for c in s:
    d[c] += 1
print d          # defaultdict(<type 'int'>, {'i': 4, 'p': 2, 's': 4, 'm': 1})
print dict(d)    # {'i': 4, 'p': 2, 's': 4, 'm': 1}
