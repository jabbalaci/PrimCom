good_shape.sh
~~~~~~~~~~~~~

#!/usr/bin/bash

sudo dpkg --configure -a\
&& sudo apt-get -f install\
&& sudo apt-get --fix-missing install\
&& sudo apt-get clean\
&& sudo apt-get update\
&& sudo apt-get upgrade\
&& sudo apt-get dist-upgrade\
&& sudo apt-get clean\
&& sudo apt-get autoremove


good_shape_safe.sh
~~~~~~~~~~~~~~~~~~

#!/usr/bin/bash

sudo dpkg --configure -a\
&& sudo apt-get -f install\
&& sudo apt-get --fix-missing install\
&& sudo apt-get update\
&& sudo apt-get upgrade\
&& sudo apt-get dist-upgrade\
&& sudo apt-get autoremove
