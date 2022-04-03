from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import datetime
import random
import re

pages = set()
random.seed(str(datetime.datetime.now()))


def get_internal_links(bs, include_url):
    """Get all internal links found on a page"""
    include_url = f'{urlparse(include_url).scheme}://{urlparse(include_url).netloc}'
    internal_links = []
    # Will find all links started with '/'
    for link in bs.find_all('a', href=re.compile(r'^(/|.*'+include_url+')')):
        if link.attrs['href'] not in internal_links:
            if link.attrs['href'].startswith('/'):
                internal_links.append(include_url+link.attrs['href'])
            else:
                internal_links.append(link.attrs['href'])
    return internal_links


def get_external_links(bs, exclude_url):
    external_links = []
    regex = re.compile('^(http|www)((?!'+exclude_url+').)*$')
    for link in bs.find_all('a', href=regex):
        if link.attrs['href'] not in external_links:
            external_links.append(link.attrs['href'])
    return external_links


def get_random_external_link(starting_page):
    try:
        html = urlopen(starting_page)
    except HTTPError or AttributeError:
        print('Something is wrong')
    else:
        bs = BeautifulSoup(html, 'html.parser')
        external_links = get_external_links(bs, urlparse(starting_page).netloc)
        if len(external_links) == 0:
            print('no external links, looking around the site for one')
            domain = f'{urlparse(starting_page).scheme}://{urlparse(starting_page).netloc}'
            internal_links = get_internal_links(bs, domain)
            try:
                return get_random_external_link(internal_links[random.randint(0, len(internal_links) - 1)])
            except ValueError:
                print('Something is wrong')
        else:
            return external_links[random.randint(0, len(external_links) - 1)]


def follow_external_only(starting_site='https://github.com'):
    external_link = get_random_external_link(starting_site)
    print(f'Random external link is: {external_link}')
    return external_link


while True:
    follow_external_only(starting_site=follow_external_only())
