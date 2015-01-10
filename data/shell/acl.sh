setfacl -R -m u:www-data:rwx $HOME/public_html/pmwiki/wiki.d

# a web application wants to read/write the sqlite.db file
setfacl -m u:www-data:rw sqlite.db
setfacl -m u:www-data:rwx .

# group: setfacl -m g:<groupid>:<rights> <file/folder>
