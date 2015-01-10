# combine PDFs into one file
pdftk *.pdf cat output all.pdf

# split to pages
pdftk in.pdf burst

# skip the first 4 pages and keep the rest
# end: last page
# r1:  reverse, last page
# r2:  reverse, the page before the last page
# etc.
pdftk in.pdf cat 5-end output out.pdf
