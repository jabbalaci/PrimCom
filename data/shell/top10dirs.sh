# LARGEST DIRECTORIES
# -------------------
# human-readable format
du -hsx * | sort -rh | head -10

# in kilobytes
du -sx * | sort -rh | head -10

# -h: display sizes in human readable format (e.g., 1K, 234M, 2G)
# -s: show only a total for each argument (summary)
# -x: skip directories on different file systems


# LARGEST FILES
# -------------
# filesizes are in bytes
find . -printf '%s %p\n' | sort -nr | head -10

# filesizes in human-readable format
# see https://github.com/jabbalaci/Bash-Utils/blob/master/top10.py
