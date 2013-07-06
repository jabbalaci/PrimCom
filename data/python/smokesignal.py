# https://github.com/shaunduncan/smokesignal
# http://www.reddit.com/r/Python/comments/1f7fuf/smokesignal_simple_python_signaling/
# related work: blinker ( http://discorporate.us/projects/Blinker/ )

from time import sleep
import smokesignal

@smokesignal.on('debug')
def verbose(val):
    print "#", val

# smokesignal.on('debug', verbose)
# smokesignal.on('debug', verbose, max_calls=5)    ## respond max. 5 times to the signal
# smokesignal.once('debug', verbose)    ## max_calls=1 this time

def main():
    for i in range(100):
        if i and i%10==0:
            smokesignal.emit('debug', i)
        sleep(.1)

##############################

if __name__ == "__main__":
    main()
