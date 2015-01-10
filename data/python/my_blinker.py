from blinker import signal

>>> started = signal('round-started')
>>> def each(round):
...     print "Round %s!" % round
...
>>> started.connect(each)

>>> def round_two(round):
...     print "This is round two."
...
>>> started.connect(round_two, sender=2)

>>> for round in range(1, 4):
...     started.send(round)
...
# Round 1!
# Round 2!
# This is round two.
# Round 3!

########## ^^^ simple example above ^^^ ##########

class One:
    def __init__(self):
        self.two = Two()
        self.two.some_signal.connect(self.callback)

    def callback(self, data):    # notice the data parameter
        print 'Called'

class Two:
    some_signal = signal('some_signal')

    def process(self):
        # Do something                                
        self.some_signal.send()

one = One()
one.two.process()

# by jcollado @ http://stackoverflow.com/questions/8594549
#
# In code above, the Two object doesn't even know if there's some other
# object interested in its internal state changes. However, it does notify
# about them by emitting a signal that might be used by other objects
# (in this case a One object) to perform some specific action.
# 
# A good example about this approach is a GUI framework. When a button
# widget is created, it's not needed to pass a callback that should be
# executed when the button is clicked. However, the button emits the
# clicked signal and whatever callback is subscribed to that signal is
# executed to perform the desired action.

# https://pypi.python.org/pypi/blinker/
