# this is NOT what you might expect:
>>> "python.json".rstrip(".json")
'pyth'

# remove suffix from the end of text ( http://stackoverflow.com/questions/1038824 ):
def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]

>>> strip_end("python.json", ".json")
'python'
