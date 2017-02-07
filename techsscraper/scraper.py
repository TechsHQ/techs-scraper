import yaml
import logging

from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings
from queue import Queue

logger = logging.getLogger(__name__)


class Scraper(object):
    def __init__(self):
        self.blogs = yaml.load(open('blogs.yaml', 'r'))
        self.q = Queue()
        for blog in self.blogs:
            self.q.put(blog)
        self.runner = CrawlerRunner(get_project_settings())
        self.concurrent_spiders = get_project_settings().get("CONCURRENT_SPIDERS", 16)
        self.remaining_spiders = self.concurrent_spiders

    def spider_closed(self, spider):
        self.run_spider_from_queue()

    def scrape_all_blogs(self):
        for _ in range(self.concurrent_spiders):
            self.run_spider_from_queue()

        reactor.run()

    def run_spider_from_queue(self):
        if self.q.empty():
            self.remaining_spiders -= 1
            if self.remaining_spiders == 0:
                logger.debug("Stop reactor")
                reactor.stop()
            return
        blog = self.q.get()
        loader = SpiderLoader(get_project_settings())
        spidercls = loader.load(self.blogs[blog]['spider'])
        crawler = Crawler(spidercls, get_project_settings())
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
        self.runner.crawl(crawler, **self.blogs[blog], blog_name=blog)
