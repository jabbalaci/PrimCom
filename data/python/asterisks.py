def foo(a, b, c):
    print a, b, c

mydict = {'a':1, 'b':2, 'c':3}
mylist = [10, 20, 30]

foo(*mydict)
# a, b, c

foo(**mydict)
# 1, 2, 3

foo(*mylist)
# 10 20 30
