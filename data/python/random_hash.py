import random

def my_hash(bits=96):
    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
    if len(s) < required_length:
        return my_hash(bits)
    else:
        return s

# print my_hash()
# 9c14dac2a6f1d65929095295    # just a sample; it's a string

## or: ##################

# You can also use simpleflake. By default it generates 64 bit
# unique IDs. The generated ID consists of 2 parts: a) timestamp,
# b) random number. It has the advantage that the generated IDs
# arrive in ascending order.
# see http://engineering.custommade.com/simpleflake-distributed-id-generation-for-the-lazy/

$ pip install simpleflake
>>> import simpleflake
>>> simpleflake.simpleflake()
3620361890155888216L    # just a sample
