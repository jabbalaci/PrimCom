import os

print os.path.join('/trash/movies', 'film.avi')    # (no trailing slash)   /trash/movies/film.avi
print os.path.join('/trash/movies/', 'film.avi')   # (with trailing slash) /trash/movies/film.avi
