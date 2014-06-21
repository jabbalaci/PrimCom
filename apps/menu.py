#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

####################
if __name__ == "__main__":
    import site
    site.addsitedir(".")
    del site
####################

from collections import OrderedDict

from lib import common

from apps import radio

menu = OrderedDict()
menu[(1, 'r')] = 'radio'


def show_menu():
    for k, v in menu.iteritems():
        print("({0})[{1}] {2}".format(k[0], k[1], v))
    print("--------")
    print("[m] menu")
    print("[q] <<")


def get_d_num(menu):
    d = {}
    for k, v in menu.iteritems():
        d[k[0]] = v
    return d


def get_d_word(menu):
    d = {}
    for k, v in menu.iteritems():
        d[k[1]] = v
    return d


def start_app(app_name):
    if app_name == 'radio':
        radio.radio_player()


def main():
    show_menu()
    d_num = get_d_num(menu)
    d_word = get_d_word(menu)
    while True:
        try:
            inp = raw_input("~~> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        if len(inp) == 0:
            continue
        elif inp == 'q':
            return
        elif inp == 'qq':
            common.my_exit(0)
        elif inp == 'm':
            show_menu()
            continue
        try:
            if inp.isdigit():
                val = d_num.get(int(inp))
            else:
                val = d_word.get(inp)
            if val is None:
                raise IndexError
        except IndexError:
            print("out of range...")
        else:
            start_app(val)

##############################################################################

if __name__ == "__main__":
    main()
