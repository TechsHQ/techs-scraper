import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from urllib.parse import urlparse

from items import BlogItem


class AtlassianSpider(scrapy.Spider):

    name = 'atlassian'

    def __init__(self, **kw):
        super(AtlassianSpider, self).__init__(**kw)
        self.blog_name = kw.get('blog_name')
        url = kw.get('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s' % url
        self.url = url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        for item in response.xpath("//div[contains(@class, 'blog-archive')]"
                                   "/div[not(contains(@class, 'pager'))]"
                                   "/div[contains(@class, 'aui-page-header')]"):
            il = ItemLoader(item=BlogItem(), response=response, selector=item)
            il.add_xpath('title', 'div/div/h2/a/text()')
            il.add_xpath('url', 'div/div/h2/a/@href')
            il.add_xpath('pub_date', 'div/div/p/text()', TakeFirst())
            yield il.load_item()
