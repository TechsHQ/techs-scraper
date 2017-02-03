# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

from util import *


class BlogItem(scrapy.Item):
    _id = scrapy.Field()
    publisher = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(clean),
                         output_processor=TakeFirst())

    url = scrapy.Field(input_processor=MapCompose(clean),
                       output_processor=TakeFirst())

    pub_date = scrapy.Field(input_processor=MapCompose(clean, serialize_date),
                            output_processor=TakeFirst())
