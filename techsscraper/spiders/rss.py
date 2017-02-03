import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from items import BlogItem


class RSSSpider(scrapy.Spider):

    name = 'rss'

    def __init__(self, **kw):
        super(RSSSpider, self).__init__(**kw)
        self.blog_name = kw.get('blog_name')
        url = kw.get('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        self.url = url

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        for item in response.xpath('//item'):
            il = ItemLoader(item=BlogItem(), response=response, selector=item)
            il.add_value('publisher', self.blog_name)
            il.add_xpath('title', 'title/text()')
            il.add_xpath('url', 'link/text()')
            il.add_xpath('pub_date', 'pubDate/text()')
            yield il.load_item()
