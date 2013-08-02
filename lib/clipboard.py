#!/usr/bin/env python

"""
Copy text to clipboards (to both of them). 
This solution here is specific to Linux.

For a platform independent solution, you can check out
https://github.com/asweigart/mapitpy/blob/master/pyperclip.py 
(I didn't try it).

# from lib.clipboard import text_to_clipboards
"""

import subprocess
from termcolor import colored


def text_to_clipboards(text, verbose=True):
    """Copy text to both clipboards."""
    to_primary(text)
    to_clipboard(text)
    if verbose:
        print bold("# copied to the clipboards")


def bold(text, color='white'):
    return colored(text, color, attrs=['bold'])
      
#############################################################################
      
def to_primary(text):
    """Write text to 'primary'."""
    xsel_proc = subprocess.Popen(['xsel', '-pi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(text)

def to_clipboard(text):
    """Write text to 'clipboard'."""
    xsel_proc = subprocess.Popen(['xsel', '-bi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(text)
    
#############################################################################
    
if __name__ == "__main__":
    text = "this should go on the clipboards"
    print text
    text_to_clipboards(text)

