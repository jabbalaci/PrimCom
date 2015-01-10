# LIST comprehension
print [x for x in range(1,10+1) if x%2==0]
# [2, 4, 6, 8, 10]

# DICT comprehension, 2.7+
print {x: 10 * x for x in range(1, 5+1)}
# {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}

# SET comprehension, 2.7+
print {10*x for x in range(1, 10+1)}
# set([100, 70, 40, 10, 80, 50, 20, 90, 60, 30])

>>> print {1, 2, 2, 3, 1}    # This is a set!
set([1, 2, 3])
