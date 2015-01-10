def inc_string(text):
    """
    Increase a lowercase string by one.

    Examples: a -> b, e -> f, z -> aa, af -> ag.
    """
    text = list(text[::-1])
    atvitel = False
    for index, c in enumerate(text):
        if index == 0 or atvitel:
            up = chr(ord(c)+1)
        if up <= 'z':
            atvitel = False
            text[index] = up
            break
        else:
            atvitel = True
            text[index] = 'a'

    if atvitel:
        text.append('a')

    return ''.join(text[::-1])
