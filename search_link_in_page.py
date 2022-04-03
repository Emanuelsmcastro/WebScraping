from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://en.wikipedia.org/wiki/Kevin_Bacon'

html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')
links = bs.find_all('a')

for link in links:
    if 'href' in link.attrs:
        print(link.attrs['href'])