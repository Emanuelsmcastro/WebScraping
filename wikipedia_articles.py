from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = 'http://en.wikipedia.org/wiki/Kevin_Bacon'
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')
regex = re.compile(r'^(/wiki/)((?!:).)*$')
links = bs.find('div', {'id': 'bodyContent'}).find_all('a', href=regex)
for link in links:
    if 'href' in link.attrs:
        print(link.attrs['href'])