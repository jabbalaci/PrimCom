# create a file of 1 MB size with random data (1,000,000 bytes)
dd if=/dev/urandom of=test.dat bs=1MB count=1

# same, file size now 1,048,576 bytes
dd if=/dev/urandom of=test.dat bs=1024K count=1
# same, 1,048,576 bytes
dd if=/dev/urandom of=test.dat bs=1M count=1

# another possibility is to fill with 0s
# ... if=/dev/zero ...

# fill up empty space with random data
dd if=/dev/urandom of=trash.dat bs=1MB; dd if=/dev/urandom of=trash2.dat
