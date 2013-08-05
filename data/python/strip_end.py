# this is NOT what you might expect:
>>> "python.json".rstrip(".json")
'pyth'

# remove suffix from the right side of text ( http://stackoverflow.com/questions/1038824 ):
def strip_right(text, suffix):
    if not text.endswith(suffix):
        return text
    # else
    return text[:len(text)-len(suffix)]

def strip_left(text, prefix):
    if not text.startswith(prefix):
        return text
    # else
    return text[len(prefix):]

>>> strip_right("python.json", ".json")
'python'

>>> strip_left("data/text/vmi.txt", "data/")
'text/vmi.txt'
