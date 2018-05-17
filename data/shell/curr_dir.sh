# path of the called script (if it's a symlink, then it's the path of the link!)
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH

# symlink is ignored this time, full path of the called script (where the symlink points to)
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH
