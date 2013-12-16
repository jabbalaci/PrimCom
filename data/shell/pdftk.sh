# combine PDFs into one file
pdftk *.pdf cat output all.pdf

# split to pages
pdftk in.pdf burst
