import untangle
 
#XML = 'examples/planet_python.xml'     # can read a file too
XML = 'http://planet.python.org/rss20.xml'
 
o = untangle.parse(XML)
for item in o.rss.channel.item:
    title = item.title.cdata
    link = item.link.cdata
    if link:
        print title
        print '   ', link
