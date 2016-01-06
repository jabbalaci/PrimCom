# browse images in the current directory
$ feh

# fullscreen, file info
$ feh -Fd

# fullscreen, file info, random order
$ feh -Fdz

# fullscreen, file info, random order, slideshow with 5 sec. delay
$ feh -Fdz -D 5

# show thumbnails
$ feh -t

# Show this image only. Browsing other files is not possible.
$ feh img.jpg

# Show img.jpg but allow browsing the other images too.
# You must write "./img.jpg" instead of "img.jpg"!
$ feh . --start-at ./img.jpg

# as before + fullscreen and file info
# or with my script:
# feh_view.sh img.jpg
$ feh . --start-at ./img.jpg -Fd

# as before + images are auto-zoomed to the window size
$ feh . --start-at ./img.jpg -FdZ
