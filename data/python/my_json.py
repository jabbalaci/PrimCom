import json
from collections import OrderedDict

# read a .json file and build an OrderedDict of it
with open(JSON) as f:
    hdict = json.load(f, object_pairs_hook=OrderedDict)

# pretty print an OrderedDict
print json.dumps(data, indent=4)

##########

d = {...}

# write nicely to a .json file
with open(JSON, 'w') as f:
    json.dump(d, f, indent=4)

##########

# JSON prettifier
python -mjson.tool ugly.json
