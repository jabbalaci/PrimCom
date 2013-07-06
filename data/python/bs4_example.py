from jabbapylib.web.web import get_page
from jabbapylib.web.scraper import bsoup4 as bs

PARSER = 'lxml'
URL = 'http://www.bookdepository.co.uk/'

def check():
    """Just an example how to use the BS4 library."""
    text = str(get_page(URL))
    soup = bs.to_soup(text, PARSER)
    book = soup.find('div', {'class' : 'module bookSmall'})
    link = book.find('a', href=True)
    print link['href']
    #
    book = soup.find('div', {'class' : 'module fullBook'})
    try:
        title = book.find('span', {'property': 'dc:title'}).text.lower()
    except:
        title = ""
    print title
    tabs = soup.find_all('div', {'class' : 'tabModules'})[-1]
    try:
        desc = tabs.find('p', {'class' : 'paragraph'}).text.lower()
    except:
        desc = ""
    print desc
