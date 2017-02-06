import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from items import BlogItem
from util import *


class AtlassianSpider(scrapy.Spider):
    name = 'atlassian'

    def __init__(self, **kw):
        super(AtlassianSpider, self).__init__(**kw)
        self.blog_name = kw.get('blog_name')
        self.url = sanatize_url(kw.get('url'))
        self.domain = get_domain(self.url)

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        for item in response.xpath("//div[contains(@class, 'blog-archive')]"
                                   "/div[not(contains(@class, 'pager'))]"
                                   "/div[contains(@class, 'aui-page-header')]"):
            loader = ItemLoader(item=BlogItem(), response=response, selector=item)
            il = loader.nested_xpath('div/div')
            il.add_value('publisher', self.blog_name)
            il.add_xpath('title', 'h2/a/text()')
            il.add_value('url', self.domain)
            il.add_xpath('url', 'h2/a/@href')
            il.add_xpath('pub_date', 'p/text()', TakeFirst())
            yield il.load_item()
