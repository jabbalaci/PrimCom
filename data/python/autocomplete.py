# http://stackoverflow.com/questions/187621/how-to-make-a-python-command-line-program-autocomplete-arbitrary-things-not-int
# http://pythonadventures.wordpress.com/2013/06/04/how-to-make-a-python-command-line-program-autocomplete-arbitrary-things/

import readline
 
addrs = ['angela@domain.com', 'michael@domain.com', 'david@test.com']
 
def completer(text, state):
    options = [x for x in addrs if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None
 
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
 
while True:
    inp = raw_input("> ")
    print "You entered", inp
