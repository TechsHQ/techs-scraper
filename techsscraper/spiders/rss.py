import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from items import BlogItem
from util import *


class RSSSpider(scrapy.Spider):
    name = 'rss'

    def __init__(self, **kw):
        super(RSSSpider, self).__init__(**kw)
        self.publisher = kw.get('blog_name')
        self.publisher_display_name = kw.get('display_name')
        self.url = sanatize_url(kw.get('url'))

    def start_requests(self):
        self.logger.info('Start scraping %s (%s)', self.publisher_display_name, self.url)
        return [Request(self.url, callback=self.parse, errback=self.error, dont_filter=True)]

    def parse(self, response):
        self.logger.info('Response from %s (%s)', self.publisher_display_name, self.url)
        for item in response.xpath('//item'):
            il = ItemLoader(item=BlogItem(), response=response, selector=item)
            il.add_value('publisher', self.publisher)
            il.add_value('publisher_display_name', self.publisher_display_name)
            il.add_xpath('title', 'title/text()')
            il.add_xpath('url', 'link/text()')
            il.add_xpath('pub_date', 'pubDate/text()')
            il.add_xpath('pub_date', 'pubdate/text()')
            blog_item = il.load_item()

            if 'url' not in blog_item:
                self.logger.debug('URL not found in blog %s (%s)', self.publisher_display_name, self.url)
                blog_item['url'] = ''.join(item.xpath('text()').extract())

            yield blog_item

    def error(self, failure):
        # log all failures
        self.logger.error('Error scraping %s (%s)\n%s', self.publisher_display_name, self.url, repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
