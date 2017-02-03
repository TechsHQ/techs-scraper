# -*- coding: utf-8 -*-

import scrapy
import pytz
from dateutil import parser
from util import *
from scrapy.loader.processors import Join, MapCompose, TakeFirst

def parse_date(t):
    return parser.parse(t).astimezone(pytz.timezone('UTC'))

class BlogItem(scrapy.Item):
    _id = scrapy.Field()
    publisher = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(clean),
                         output_processor=TakeFirst())

    url = scrapy.Field(input_processor=MapCompose(clean),
                       output_processor=Join(''))

    pub_date = scrapy.Field(input_processor=MapCompose(clean, parse_date),
                            output_processor=TakeFirst())
