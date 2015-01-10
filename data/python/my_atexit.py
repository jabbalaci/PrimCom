import atexit

def cleanup():
    remove_lock()

##########

if __name__ == "__main__":
    atexit.register(cleanup)
    main()

==============================

def goodbye(name, adjective):
    print 'Goodbye, %s, it was %s to meet you.' % (name, adjective)

atexit.register(goodbye, 'Donny', 'nice')
