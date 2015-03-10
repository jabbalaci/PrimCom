# make wget silent (verbosity OFF)
wget --quiet URL

# print result to stdout
wget -qO- URL

# mirror a website for local use
wget -c --mirror -p --html-extension --convert-links --no-parent $url

# spider a website and get the URLs only (-l2: max. recursion depth is 2)
wget --spider --force-html -r -l2 $url 2>&1 | grep '^--' | awk '{ print $3  }'

# using wget to recursively fetch a directory with arbitrary files in it
wget -c --mirror -p --html-extension --convert-links --no-parent --reject "index.html*" $url
