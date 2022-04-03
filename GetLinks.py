from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import datetime
import re

random.seed(str(datetime.datetime.now()))


def getLinks(article_url):
    url = f'http://en.wikipedia.org{article_url}'
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    regex = re.compile(r'^(/wiki/)((?!:).)*$')
    _links = bs.find('div', {'id': 'bodyContent'}).find_all('a', href=regex)
    return _links


links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    new_article = links[random.randint(0, len(links) - 1)].attrs['href']
    print(new_article.encode('utf-8'))
    links = getLinks(new_article)
