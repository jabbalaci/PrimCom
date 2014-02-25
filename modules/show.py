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

from jinja2 import Environment, FileSystemLoader

import config as cfg
from lib import clipboard, common, simpleflake


TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader("{root}/modules/templates".format(root=cfg.ROOT)),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def show():
    text = clipboard.read_primary()
    if not text:
        print("Warning! The primary clipboard is empty.")
        return
    #
    context = {
        'link': text
    }
    fname = "/tmp/{id}.html".format(id=simpleflake.simpleflake(hexa=True))

    with open(fname, 'w') as f:
        html = render_template('link.html', context)
        f.write(html)

    common.open_url(fname)

##############################################################################

if __name__ == "__main__":
    show()
