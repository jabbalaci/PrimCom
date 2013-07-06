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
