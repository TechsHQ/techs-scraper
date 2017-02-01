import scrapy
from scrapy.http import Request
from urllib.parse import urlparse

from util import clean
from items import BlogItem


class AtlassianSpider(scrapy.Spider):

    name = 'atlassian'

    def __init__(self, **kw):
        super(AtlassianSpider, self).__init__(**kw)
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
            yield BlogItem(
                title=clean(item.xpath('div/div/h2/a/text()').extract_first()),
                url=clean(self.domain + item.xpath('div/div/h2/a/@href').extract_first()),
                pub_date=clean(item.xpath('div/div/p/text()').extract_first())
            )