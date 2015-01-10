# tip from here: https://stackoverflow.com/questions/2720014
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
