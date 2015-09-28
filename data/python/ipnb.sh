# install v2
sudo apt-get install ipython-notebook

# install v3
sudo apt-get install ipython3-notebook

# create profile
ipython profile create

# customize dir. for notebooks
# edit ~/.config/ipython/profile_default/ipython_notebook_config.py
c.NotebookManager.notebook_dir = u'/home/jabba/Dropbox/ipython_notebooks'

# start v2
ipython notebook

# start v3
ipython3 notebook
