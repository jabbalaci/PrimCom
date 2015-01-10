# by segfaultzen @reddit
function workon () {
    if [[ -z $1 ]] ; then
        echo -e "\nUsage:\n\tworkon <virtualenv>\n"
    else
        source ~/Development/python/virtualenvs/$1/bin/activate ;
    fi
}
