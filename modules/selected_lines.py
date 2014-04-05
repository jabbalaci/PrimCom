#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

from lib.clipboard import text_to_clipboards


def get_pages(s, last):
    """
    Having a compact description of line numbers (s), create a list
    of line numbers. "last" contains the number of lines altogether.

    Examples: 1,3-5    -> [1,3,4,5]
              2-       -> [2,3,4,5], if the file has 5 lines
    """
    s = s.strip()
    if len(s) == 0:
        return []

    li = []
    #
    for piece in s.split(','):
        pos = piece.find('-')
        if pos > -1:
            n1 = int(piece[:pos])
            if piece.endswith('-'):
                n2 = last
            else:
                n2 = int(piece[pos+1:])
            li.extend(range(n1, n2+1))
        else:
            li.append(int(piece))
    return li


def get_selected_lines(flines, pages):
    """
    Get the selected lines from the lines of a file.

    Example: if pages is [1, 2], then return the first two
    lines of the file.

    flines: lines of a file in a list
    pages: line numbers in a list
    """
    pages = set(pages)
    return [line for i, line in enumerate(flines, start=1) if i in pages]


def do_action(lines, action):
    """
    We have some lines from a file and perform an action on them.

    TODO: it's not yet ready. When I meet new needs, I will extend this method.
    """
    text = ''.join(lines).rstrip('\n')
    if action == 'cb':
        # copy text to clipboard
        text_to_clipboards(text)
    elif action == 'cb(>)':
        # add 4 leading spaces to each line (facilitate code insert in markdown)
        text = '\n'.join(['    ' + line for line in text.split('\n')])
        text_to_clipboards(text)
    elif action == 'sh':
        if len(lines) == 1:
            if text.startswith('$ '):
                text = text[2:]
            os.system(text)
        else:
            print('Warning! This action is not yet implemented.')
            print("Check out the selected_lines.py file's do_action() method.")


def process_selected_lines(inp, fname):
    """
    We have a command like "l2.cb", which means: copy the 2nd line
    of the file to the clipboard. Process it.

    inp: user input
    fname: the absolute path of the file that we want to work on
    """
    pos = inp.find('.')
    group1 = inp[1:pos]
    action = inp[pos+1:]
    flines = open(fname).readlines()
    #
    pages = get_pages(group1, len(flines))
    selected_lines = get_selected_lines(flines, pages)
    do_action(selected_lines, action)
