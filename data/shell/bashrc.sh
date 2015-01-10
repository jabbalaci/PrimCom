#############################################################################
# Jabba (20130611)
#############################################################################
#umask 077

#set -o vi
EDITOR=/usr/bin/vim
export EDITOR

JAVA_HOME=/opt/java
JDK_HOME=$JAVA_HOME
PATH=$JAVA_HOME/bin:$PATH:$HOME/bin:$HOME/bin.python

export JAVA_HOME JDK_HOME PATH

#function msdos_pwd
#{
#    local dir="`pwd`"
#    dir=${dir/$HOME/'~'}
#
#    echo $dir | tr '/' '\\'
#}
#
#export PS1='C:`msdos_pwd`> '

# finance project, HTML to PDF
#PATH=$PATH:/opt/wkhtmltopdf
#export PATH

PYTHONPATH=$PYTHONPATH:$HOME/python/lib/jabbapylib:$HOME/python/lib
PYTHONPATH=$PYTHONPATH:$HOME/python/lib/google_appengine
export PYTHONPATH

PYPY=/opt/pypy/bin
PATH=$PATH:$PYPY
export PATH

#PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/dist-packages/spyderlib
#export PYTHONPATH

# don't create .pyc and .pyo files
#PYTHONDONTWRITEBYTECODE=True
#export PYTHONDONTWRITEBYTECODE

export PYTHONSTARTUP=$HOME/.pythonstartup

PATH=$PATH:$HOME/lib/google_appengine
export PATH

# Android's Video directory
A='/media/jabba/2B9A-EB28/Video'
export A

PATH=$PATH:/opt/chromedriver
export PATH

# deactivate that the screen goes blank in 10 minutes
#xset s 0 0

# pless (pygmentized less)
export LESS='-R'

alias md='mkdir'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias d='ls -al'
#alias mc='. /usr/share/mc/bin/mc-wrapper.sh'
alias mc='. /usr/local/libexec/mc/mc-wrapper.sh'
alias run='chmod u+x'
alias rid='chmod 644'
alias ridd='chmod 755'
alias gq='gqview &'
alias tailf='tail -f'
alias cls='clear'
alias nh='nautilus . 2>/dev/null'
alias gt='gthumb &'
alias p='python'
alias pudb='python -m pudb'
alias p3='python3'
alias bpy='bpython'
alias ipy='ipython'
alias th='echo "cls; cd `pwd`"'
alias kr='krusader &'
alias kill9='kill -9'
alias sshow_r='feh -zsZFD 5 .'
alias sshow_n='feh -FD 5 .'
alias ed='$HOME/bin/st'
alias tm='tmux'
alias t='task'
alias killvlc='kill -9 `ps ux | grep vlc | grep -v grep | tr -s " " | cut -d" " -f2`'
alias killmplayer='ps ux | grep mplayer | grep -v grep | tr -s " " | cut -d" " -f2 | xargs kill -9'
alias k='konsole 2>/dev/null &'
alias Q='tail -f $HOME/bin/copy_queue/daemon.log'
alias sagi='sudo apt-get install'
alias pcat="pygmentize -f terminal256 -O style=native -g"
alias beep="mplayer -ao alsa $HOME/bin/alert.wav &>/dev/null"

# .xsession-errors can grow huge... remove it
if [ ! -h $HOME/.xsession-errors ]
then
    /bin/rm $HOME/.xsession-errors 2>/dev/null
    ln -s /dev/null $HOME/.xsession-errors 2>/dev/null
fi
 
if [ ! -h $HOME/.xsession-errors.old ]
then
    /bin/rm $HOME/.xsession-errors.old 2>/dev/null
    ln -s /dev/null $HOME/.xsession-errors.old 2>/dev/null
fi

/usr/games/fortune | /usr/games/cowthink
