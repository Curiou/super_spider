# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ElemaItem(scrapy.Item):
    # define the fields for your item here like:
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    foods_name = scrapy.Field()
    pass
