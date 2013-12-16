# copy string to "primary" clipboard
echo "hello" | xsel -pi
# copy string to "clipboard" clipboard
echo "hello" | xsel -bi
# print the content of the clipboards
# primary and clipboard, respectively
xsel -op
xsel -ob
