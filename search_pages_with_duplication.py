from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import datetime
import re

pages = set()


def getLinks(article_url):
    global pages
    url = f'http://en.wikipedia.org{article_url}'
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    regex = re.compile(r'^(/wiki/)')
    _links = bs.find_all('a', href=regex)
    for link in _links:
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                new_page = link.attrs['href']
                print(new_page)
                pages.add(new_page)
                getLinks(new_page)


getLinks('')


