#!/usr/bin/env python
# encoding: utf-8

"""
Fancy logos for PrimCom.

Most of the logos were created with
http://patorjk.com/software/taag

One logo is my own creation :)
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from random import choice, randrange

import config as cfg
from lib.common import bold, my_shuffle


logos = [
r"""
 _____     _       _____
|  _  |___|_|_____|     |___ _____
|   __|  _| |     |   --| . |     |
|__|  |_| |_|_|_|_|_____|___|_|_|_| {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
  ___     _       ___
 | _ \_ _(_)_ __ / __|___ _ __
 |  _/ '_| | '  \ (__/ _ \ '  \
 |_| |_| |_|_|_|_\___\___/_|_|_| {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
   ___      _       _____
  / _ \____(_)_ _  / ___/__  __ _
 / ___/ __/ /  ' \/ /__/ _ \/  ' \
/_/  /_/ /_/_/_/_/\___/\___/_/_/_/ {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
,------.        ,--.           ,-----.
|  .--. ',--.--.`--',--,--,--.'  .--./ ,---. ,--,--,--.
|  '--' ||  .--',--.|        ||  |    | .-. ||        |
|  | --' |  |   |  ||  |  |  |'  '--'\' '-' '|  |  |  |
`--'     `--'   `--'`--`--`--' `-----' `---' `--`--`--' {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
██████╗ ██████╗ ██╗███╗   ███╗ ██████╗ ██████╗ ███╗   ███╗
██╔══██╗██╔══██╗██║████╗ ████║██╔════╝██╔═══██╗████╗ ████║
██████╔╝██████╔╝██║██╔████╔██║██║     ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██╗██║██║╚██╔╝██║██║     ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║██║ ╚═╝ ██║╚██████╗╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝ {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
╔═╗┬─┐┬┌┬┐╔═╗┌─┐┌┬┐
╠═╝├┬┘││││║  │ ││││
╩  ┴└─┴┴ ┴╚═╝└─┘┴ ┴ {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
:::::::::  :::::::::  ::::::::::: ::::    ::::   ::::::::   ::::::::  ::::    ::::
:+:    :+: :+:    :+:     :+:     +:+:+: :+:+:+ :+:    :+: :+:    :+: +:+:+: :+:+:+
+:+    +:+ +:+    +:+     +:+     +:+ +:+:+ +:+ +:+        +:+    +:+ +:+ +:+:+ +:+
+#++:++#+  +#++:++#:      +#+     +#+  +:+  +#+ +#+        +#+    +:+ +#+  +:+  +#+
+#+        +#+    +#+     +#+     +#+       +#+ +#+        +#+    +#+ +#+       +#+
#+#        #+#    #+#     #+#     #+#       #+# #+#    #+# #+#    #+# #+#       #+#
###        ###    ### ########### ###       ###  ########   ########  ###       ### {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
 ______        __            ______
|   __ \.----.|__|.--------.|      |.-----.--------.
|    __/|   _||  ||        ||   ---||  _  |        |
|___|   |__|  |__||__|__|__||______||_____|__|__|__| {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
  _______      __          _______
 |   _   .----|__.--------|   _   .-----.--------.
 |.      |   _|  |        |.   ___|  _  |        |
 |.  ____|__| |__|__|__|__|.  |___|_____|__|__|__|
 |:  |                    |:      |
 |::.|                    |::.. . |
 `---'                    `-------' {v}
""".lstrip('\n').format(v=cfg.__version__),
# geek version:
r"""
80 114 105 109 67 111 109 {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
  ____       _            ____
 |  _ \ _ __(_)_ __ ___  / ___|___  _ __ ___
 | |_) | '__| | '_ ` _ \| |   / _ \| '_ ` _ \
 |  __/| |  | | | | | | | |__| (_) | | | | | |
 |_|   |_|  |_|_| |_| |_|\____\___/|_| |_| |_| {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
 __   __           __   __
|__) |__) |  |\/| /  ` /  \  |\/|
|    |  \ |  |  | \__, \__/  |  | {v}
""".lstrip('\n').format(v=cfg.__version__),
#
r"""
 __       __
|__)_. _ /   _  _
|  | ||||\__(_)||| {v}
""".lstrip('\n').format(v=cfg.__version__),
# this one was designed by me:
r"""
┌─────┐           ┌─────┐
│ ┌─┐ │           │ ┌───┘
│ └─┘ ├───┬─┬─────┤ │   ┌─────┬─────┐
│ ┌───┤ ┌─┼─┤ ╷ ╷ │ │   │ ┌─┐ │ ╷ ╷ │
│ │   │ │ │ │ │ │ │ └───┤ └─┘ │ │ │ │
└─┘   └─┘ └─┴─┴─┴─┴─────┴─────┴─┴─┴─┘ {v}
""".lstrip('\n').format(v=cfg.__version__),
# this rainbow colored logo MUST BE THE LAST ONE
"""
[1;38;5;33m[0m[1;38;5;39m┌─────┐           ┌─────┐[0m[1;38;5;45m[0m
[1;38;5;51m[0m[1;38;5;50m│ ┌─┐ │           │ ┌───┘[0m[1;38;5;49m[0m
[1;38;5;48m[0m[1;38;5;47m│ └─┘ ├───┬─┬─────┤ │   ┌─────┬─────┐[0m[1;38;5;46m[0m
[1;38;5;82m[0m[1;38;5;118m│ ┌───┤ ┌─┼─┤ ╷ ╷ │ │   │ ┌─┐ │ ╷ ╷ │[0m[1;38;5;154m[0m
[1;38;5;190m[0m[1;38;5;226m│ │   │ │ │ │ │ │ │ └───┤ └─┘ │ │ │ │[0m[1;38;5;220m[0m
[1;38;5;214m[0m[1;38;5;208m└─┘   └─┘ └─┴─┴─┴─┴─────┴─────┴─┴─┴─┘ {v}[0m[1;38;5;202m[0m
""".lstrip('\n').format(v=cfg.__version__),
]


def header():
    """
    Print a fancy header. The rainbow colored logo only looks good
    with dark background. If the background is light, skip it.
    """
    rainbow_index = len(logos) - 1
    if cfg.g.BACKGROUND == cfg.DARK:
        # include the rainbow
        indexes = list(range(len(logos)))
    else:
        # exclude the rainbow
        indexes = list(range(len(logos)-1))

    pos = choice(my_shuffle(indexes))
    if pos == rainbow_index:
        print(logos[pos])
    else:
        col = cfg.colors[cfg.g.BACKGROUND]["header"]
        print(bold(logos[pos], col))


#def header(version):
#    s = "PrimCom {v}".format(v=version)
#    size = len(s)
#    horizontal = '+' + '-' * (size + 2) + '+'
#    col = cfg.colors[cfg.g.BACKGROUND]["header"]
#    print(bold(horizontal, col))
#    print(bold('| ' + s + ' |', col))
#    print(bold(horizontal, col))
