import yaml

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def scrape_all_blogs():
    blogs = yaml.load(open('../blogs.yaml', 'r'))

    process = CrawlerProcess(get_project_settings())

    for blog in blogs:
        process.crawl(blogs[blog]['spider'], url=blogs[blog]['url'])

    process.start()
