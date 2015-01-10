# custom exception
class MyException(Exception):
    pass

try:
    if condition:
        raise MyException    # raise custom exception
    # ...
except MyException:
    print "Oops!..."

# see also http://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python

# ~~~~~~~~~~~~~~~~~~~~

try:
    import something
except ImportError as e:
    print 'Import problem: {e}'.format(e=e)
