# PrimCom

PrimCom is a personal _knowledge base manager_, primarily made for programmers. It is meant to be running in a terminal, thus you can access and consult it quickly while working.

### Motivation

There are lots of code snippets that I use often but I couldn't reproduce them easily by heart. When I need
such a piece of code, either I look it up on my blog (if I had written about it), or Google it. When I see the code, I remember it and I can modify it to my needs. However, looking up something on the Internet can take time (at least 30-60 seconds).

With PrimCom you can collect _your own code snippets_ with _your own examples_. You can assign tags to them and find them easily later. PrimCom can perform two main actions: print the content of a file, or open a web page.

PrimCom has several useful features. It has tab completion; it can copy the content of a file to the clipboard; it can syntax highlight your code snippets; it even has a built-in radio player, etc. See the built-in help for a detailed list.

### Quick start

Open a terminal with _dark_ background and launch PrimCom:

    $ ./h.py

If you prefer light background, use the `light()` command or modify directly the `config.py` file.

Type `h` for help, `d` for the list of available tags.

### Screenshots

With dark background:
![dark background](https://dl.dropboxusercontent.com/u/144888/wordpress/20130802-PrimCom/pc01.png)

With light background:
![light background](https://dl.dropboxusercontent.com/u/144888/wordpress/20130802-PrimCom/pc02.png)

### Requirements

The project was developed under Ubuntu GNU/Linux with Python 2.7. It is suggested that you install the following packages (via apt-get):
* python-pygments (for syntax highlighting)
* xsel (for copying to the clipboard)
* mplayer2 (for the radio)
* python-psutil (for process manipulation)

## Details

To learn more about PrimCom, refer to this page: http://jabbalaci.github.io/PrimCom.

