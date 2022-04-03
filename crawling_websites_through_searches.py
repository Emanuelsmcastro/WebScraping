import requests
from bs4 import BeautifulSoup


class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f'New article found for topic: {self.topic}\nTITLE: {self.title}\nBODY: {self.body}'
              f'\nURL: {self.url}')


class WebSite:
    def __init__(self, name, url, search_url, result_listing, result_url, absolute_url, title_tag,
                 body_tag):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.result_listing = result_listing
        self.result_url = result_url
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Crawler:
    @staticmethod
    def get_page(url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    @staticmethod
    def safe_get(page_obj, selector):
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            return child_obj[0].get_text()
        return ''

    def search(self, _topic, site):
        bs = self.get_page(site.search_url + _topic)
        search_results = bs.select(site.result_listing)
        for result in search_results:
            try:
                url = result.select(site.result_url)[0].attrs["href"]
            except:
                return
            if site.absolute_url:
                bs = self.get_page(url)
            else:
                bs = self.get_page(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping...')
                return
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(_topic, title, body, url)
                content.print()


crawler = Crawler()

site_data = [
    ['O\'Reilly Media', 'https://oreilly.com', 'https://ssearch.oreilly.com/?q=', 'article.product-result',
     'p.title a', True, 'h1', 'section#product-description'],
    ['Reuters', 'https://reuters.com', 'https://www.reuters.com/search/news?blob=', 'div.search-result-content',
     'h3.search-result-title a', False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'https://www.brookings.edu', 'https://www.brookings.edu/search/?s=', 'div.list-content article',
     'h4.title a', True, 'h1', 'div.post-body']
]
sites = []
for row in site_data:
    sites.append(WebSite(row[0], row[1], row[2], row[3], row[4], row[5],
                         row[6], row[7]))

topics = ['python', 'data science', 'arduino']
for topic in topics:
    print(f'GETTING INFO ABOUT: {topic}')
    for target_site in sites:
        crawler.search(topic, target_site)

