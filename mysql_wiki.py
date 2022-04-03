from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re


def connection(host='127.0.0.1', user='root', passwd='Emanuel2486179300!', db='mysql', charset='utf8'):
    return pymysql.connect(host=host,
                           user=user,
                           passwd=passwd,
                           db=db,
                           charset=charset)


def store(title, content):
    with connection().cursor() as cur:
        cur.execute('USE scraping')
        cur.execute(f'INSERT INTO pages (title, content) VALUES ("{title}", "{content}")')
        cur.connection.commit()


def get_links(article_url):
    html = urlopen('https://en.wikipedia.org' f'{article_url}')
    bs = BeautifulSoup(html, 'html.parser')
    try:
        title = bs.find('h1').get_text()
        content = bs.find('div', {'id': 'mw-content-text'}).find('p').get_text()
    except:
        pass
    else:
        store(title, content if content != '\n' else 'None')
        regex = re.compile(r'^(/wiki/)((?!:).)*$')
        return bs.find('div', {'id': 'bodyContent'}).findAll('a', href=regex)


with connection() as conn:
    cursor = conn.cursor()
    links = get_links('/wiki/Kevin_Bacon')
    random.seed(str(datetime.datetime.now()))
    try:
        while len(links) > 0:
            new_article = links[random.randint(0, len(links) - 1)].attrs['href']
            print(new_article)
            links = get_links(new_article)
    except:
        pass
