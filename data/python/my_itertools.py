import itertools

print list(itertools.product('ABCD', repeat=2))
# [('A', 'A'), ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'C'), ('C', 'D'), ('D', 'A'), ('D', 'B'), ('D', 'C'), ('D', 'D')]
print list(itertools.permutations('ABCD', 2))
# [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'C'), ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'A'), ('D', 'B'), ('D', 'C')]
print list(itertools.combinations('ABCD', 2))
# [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
print list(itertools.combinations_with_replacement('ABCD', 2))
# [('A', 'A'), ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'C'), ('C', 'D'), ('D', 'D')]
print list(itertools.izip('ABCD', 'xy'))
# [('A', 'x'), ('B', 'y')]

name_generator = itertools.imap("name-{}".format, itertools.count())
for _ in range(3):
    print next(name_generator)
# name-0
# name-1
# name-2

# related tag: static variable

# see also:
# http://docs.python.org/2/library/itertools.html
# http://docs.python.org/2/library/itertools.html#itertools-recipes
# http://pymotw.com/2/itertools/
