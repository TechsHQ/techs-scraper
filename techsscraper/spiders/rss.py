import scrapy
from scrapy.http import Request

from util import clean
from items import BlogItem


class RSSSpider(scrapy.Spider):

    name = 'rss'

    def __init__(self, **kw):
        super(RSSSpider, self).__init__(**kw)
        url = kw.get('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        self.url = url

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        for item in response.xpath('//item'):
            yield BlogItem(
                title=clean(item.xpath('title/text()').extract_first()),
                url=clean(item.xpath('link/text()').extract_first()),
                pub_date=clean(item.xpath('pubDate/text()').extract_first() or item.xpath('pubdate/text()').extract_first()),
            )
