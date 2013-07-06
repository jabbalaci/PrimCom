import curses

def main(screen):
    """screen is a curses screen passed from the wrapper"""
    # It will do curses.cbreak(), curses.noecho() and curses_screen.keypad(1) on init 
    # and reverse them on exit, even if the exit was an exception.

if __name__ == '__main__':
    curses.wrapper(main)

===================

Manually:

import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
...
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
