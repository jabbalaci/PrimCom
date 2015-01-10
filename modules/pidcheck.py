from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from threading import Thread
from time import sleep

import psutil

import config as cfg
from lib.common import exit_signal, my_exit, play_audio

##########

class PidChecker(Thread):
    def __init__(self):
        super(PidChecker, self).__init__()
        self.checklist = set()
        self.running = True
        exit_signal.connect(self.terminate)

    def add(self, pid):
        try:
            pid = int(pid)
        except ValueError:
            print('Hm?')
            return
        # else
        try:
            self.checklist.add(psutil.Process(pid))
            if not self.isAlive():
                self.start()
        except psutil._error.NoSuchProcess:
            print('Warning: no such PID.')

    def remove(self, pid):
        try:
            pid = int(pid)
        except ValueError:
            print('Hm?')
            return
        # else
        for proc in self.checklist:
            if pid == proc.pid:
                self.checklist.remove(proc)
                break
        else:
            print('Warning: no such PID.')

    def stop(self):
        self.running = False

    def terminate(self, data):
        if self.isAlive():
            self.stop()
            self.join()

    def contents(self):
        if not self.checklist:
            print('<empty>')
        else:
            for p in sorted(self.checklist, key=lambda p: p.pid):
                print('*', p)

    def run(self):
        while self.running:
            pids = set(psutil.get_pid_list())
            try:
                for proc in self.checklist:
                    pid = proc.pid
                    if pid not in pids:
                        play_beep()
                        notify_send("Process with PID {pid} stopped.".format(pid=pid))
                        self.checklist.remove(proc)
            except RuntimeError:
                continue
            sleep(1)

pid_checker = PidChecker()

##########

def play_beep():
    play_audio(cfg.ALERT)


def notify_send(msg):
    logo = "{root}/assets/logo.xpm".format(root=cfg.ROOT)
    main = "PrimCom Alert"
    sub = msg
    cmd = 'notify-send -i {logo} "{main}" "{sub}"'.format(logo=logo,
                                                          main=main, sub=sub)
    os.system(cmd)


def watch_pid():
    pid_checker.contents()
    try:
        pid = int(raw_input("PID: ").strip())
    except ValueError:
        print('Wat?')
        return
    except (KeyboardInterrupt, EOFError):
        print()
        return
    # else
    if pid not in psutil.get_pid_list():
        print('Warning: no such PID.')
        return
    # else
    pid_checker.add(pid)


def pid_alert():
    text = """
(1) ps
(2) adjust alert volume
(3) set pid to watch (add:<pid>, remove:<pid>)
(4) list of watched processes (d)
[m] this menu
[q] <<
""".strip()
    print(text)
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if len(inp) == 0:
            continue
        elif inp == 'q':
            return
        elif inp == 'qq':
            my_exit(0)
        elif inp == 'm':
            print(text)
        elif inp.startswith('!'):
            cmd = inp[1:]
            os.system(cmd)
        elif inp in ('1', 'ps'):
            os.system("ps ux")
        elif inp == '2':
            play_beep()
        elif inp == '3':
            watch_pid()
        elif inp in ('4', 'd'):
            pid_checker.contents()
        elif inp.startswith('add:'):
            pid_checker.add(inp[inp.find(':')+1:])
        elif inp.startswith('remove:'):
            pid_checker.remove(inp[inp.find(':')+1:])
        else:
            print('Wat?')
