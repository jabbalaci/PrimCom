# from http://bhfsteve.blogspot.hu/2014/07/embedding-python-in-bash-scripts.html?m=1
#############
# Example 1 #
#############
#!/bin/bash

function current_datetime {
python - <<END
import datetime
print datetime.datetime.now()
END
}

# Call it
current_datetime

# Call it and capture the output
DT=$(current_datetime)
echo Current date and time: $DT


#############
# Example 2 # (passing arguments to the wrapping function)
#############
#!/bin/bash

function line {
PYTHON_ARG="$1" python - <<END
import os
line_len = int(os.environ['PYTHON_ARG'])
print '-' * line_len
END
}

# Do it one way
line 80

echo 'Handy'

# Do it another way
echo $(line 80)
