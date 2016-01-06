# resize all images to width 1200 by keeping the aspect ratio
for i in *.JPG; do echo $i; convert -resize 1200 $i a/$i; done
