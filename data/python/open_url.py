import os

def open_url(url):
    #webbrowser.open_new_tab(url)
    os.system('firefox -url "{url}" 2>/dev/null'.format(url=url))
