# iotop can be run in batch mode instead of the default interactive mode
# using the -b option. -o is used to show only processes actually doing I/O,
# and -qqq is to suppress column names and I/O summary.
# from https://wiki.archlinux.org/index.php/SSD
sudo iotop -boqqq
