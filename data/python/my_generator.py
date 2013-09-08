def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a+b
 
f = fib()
for i in range(10):    # print the first ten Fibonacci numbers
    print f.next(),    # 0 1 1 2 3 5 8 13 21 34

####################

# loop through a generator
for item in function_that_returns_a_generator(param1, param2):
    print item
