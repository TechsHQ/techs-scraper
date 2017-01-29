# -*- coding: utf-8 -*-

import scrapy


class BlogItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    pub_date = scrapy.Field()
