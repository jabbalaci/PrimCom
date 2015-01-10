groups           # groups of current user
groups  jabba    # groups of user jabba

sudo  usermod  -a  -G  group  user    # add user to group

# remove user from group
# (1) list all groups except the one from where you want to remove the user
sudo  usermod  -G  all,existing,groups,except,for,group  user
# (2) remove user from group
sudo  gpasswd  -d  user  group
