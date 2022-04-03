import requests
from bs4 import BeautifulSoup


class Content:
    def __init__(self, url, title, body):
        self._url = url
        self._title = title
        self._body = body

    def print(self):
        print(f'URL: {self._url}'
              f'\nTITLE: {self._title}'
              f'\nBODY: {self._body}')


class WebSite:
    def __init__(self, name, url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Crawler:
    @staticmethod
    def get_page(url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f'Error founded: {e}')
            return None
        return BeautifulSoup(req.text, 'html.parser')

    @staticmethod
    def safe_get(page_obj, selector):
        selected_elements = page_obj.select(selector)
        if selected_elements is not None and len(selected_elements) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elements])
        return ''

    def parse(self, site, url):
        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()


crawler = Crawler()
site_data = [
    ['O\'Reilly Media', 'https://www.oreilly.com', 'h1', 'section#product-description'],
    ['Reuters', 'https://www.reuters.com', 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'https://www.brookings.edu', 'h1', 'div.post-body'],
    ['New York Times', 'https://www.nytimes.com', 'h1', 'p.story-content']
]

websites = []
for row in site_data:
    websites.append(WebSite(row[0], row[1], row[2], row[3]))

crawler.parse(websites[0], 'https://www.oreilly.com/products/books-videos.html')
crawler.parse(websites[1], 'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(websites[2], 'http://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy'
                           '-education/')
crawler.parse(websites[3], 'http://www.nytimes.com/2018/01/28/business/energy-environment/oil-boom.html')
