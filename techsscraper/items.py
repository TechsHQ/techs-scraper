# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from processors import *


class BlogItem(scrapy.Item):
    _id = scrapy.Field()
    publisher = scrapy.Field(output_processor=TakeFirst())
    publisher_display_name = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(clean),
                         output_processor=TakeFirst())

    url = scrapy.Field(input_processor=MapCompose(clean, check_url),
                       output_processor=Join(''))

    pub_date = scrapy.Field(input_processor=MapCompose(clean, parse_date),
                            output_processor=TakeFirst())
