import re
import requests
from bs4 import BeautifulSoup

class WebSite:
    def __init__(self, name, url, target_pattern, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f'URL: {self.url}\nTITLE: {self.title}\nBODY: {self.body}')


class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    @staticmethod
    def get_page(url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as e:
            return print(f'ERROR: {e}')
        return BeautifulSoup(req.text, 'html.parser')

    @staticmethod
    def safe_get(page_obj, selector):
        selected_elements = page_obj.select(selector)
        if selected_elements is not None and len(selected_elements) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elements])
        return ''

    def parse(self, url):
        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, self.site.title_tag)
            body = self.safe_get(bs, self.site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        bs = self.get_page(self.site.url)
        target_pages = bs.findAll('a', href=re.compile(self.site.target_pattern))
        for target_page in target_pages:
            target_page_attrs = target_page.attrs['href']
            if target_page_attrs not in self.visited:
                self.visited.append(target_page_attrs)
                if not self.site.absolute_url:
                    target_page_attrs = f'{self.site.url}{target_page}'
                self.parse(target_page_attrs)


reuters = WebSite('Reuters', 'https://www.reuters.com', r'^(/article/)', False, 'h1',
                  'div.StandardArticleBody_body_1gnLA')
crawler = Crawler(reuters)
crawler.crawl()
