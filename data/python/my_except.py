# found at http://stackoverflow.com/questions/855759/python-try-else

# The statements in the else block are executed if execution falls off 
# the bottom of the try, i.e. if there was no exception.

try:
    operation_that_can_throw_ioerror()
except IOError:
    handle_the_exception_somehow()
else:
     # we don't want to catch the IOError if it's raised
    another_operation_that_can_throw_ioerror()
finally:
    something_we_always_need_to_do()


# The else lets you make sure:
# 
# * another_operation_that_can_throw_ioerror() is only run if there's no exception,
# * it's run before the finally block, and
# * any IOErrors it raises aren't caught here
