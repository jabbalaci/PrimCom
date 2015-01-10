import urlparse

base = 'http://example.com/'
fname = 'img.jpg'

print urlparse.urljoin(base, fname)    # http://example.com/img.jpg
