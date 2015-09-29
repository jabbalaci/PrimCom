##########################
## New IPython Notebook ##
##########################

$ sudo pip install jupyter
$ sudo pip3 install jupyter

# Enable Python 3 kernel
mkdir -p ~/.ipython/kernels/python3
# create the file ~/.ipython/kernels/python3/kernel.json with the content:
{
 "display_name": "IPython (Python 3)",
 "language": "python",
 "argv": [
  "python3",
  "-c", "from IPython.kernel.zmq.kernelapp import main; main()",
  "-f", "{connection_file}"
 ],
 "codemirror_mode": {
  "version": 2,
  "name": "ipython"
 }
}

# specify default directory:
# add this line to  ~/.jupyter/jupyter_notebook_config.py :
c.NotebookApp.notebook_dir = u'/home/jabba/Dropbox/ipython_notebooks'
# notice it's called ...App...

# open a given directory:
$ jupyter notebook --notebook-dir <dir>

# then switch between Python 2 and Python 3 kernels in Jupyter


##########################
## Old IPython Notebook ##
##########################

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
