import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

regex = re.compile(r'\.\./img/gifts/img.\.jpg')

url = 'https://pythonscraping.com/pages/page3.html'
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img', {'src': regex})

for image in images:
    print(image['src'])
