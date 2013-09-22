from threading import Thread, Lock

THREADS = 5
lock = Lock()
threads = []

class DownLoadThread(Thread):
    def __init__(self, thread_id):
        super(DownLoadThread, self).__init__()
        self.thread_id = thread_id

    def run(self):
        with lock:
            print "{tid}: started".format(tid=self.thread_id)
        sleep(randint(1,3))
        with lock:
            print "{tid}: stopped".format(tid=self.thread_id)


def main():
    global threads
    #
    for i in xrange(THREADS):
        t = DownLoadThread(i)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print "# END"

####################
## simple version ##
####################

def this_should_run_in_the_background():
    # some code

def main():
    # start a function in a thread
    Thread(target=this_should_run_in_the_background).start()
