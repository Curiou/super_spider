# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AssettransactionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asset_no = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    subject = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    transfer_price = scrapy.Field()
    transfer_rate = scrapy.Field()
    description = scrapy.Field()
    remark = scrapy.Field()
    information = scrapy.Field()
    total_review = scrapy.Field()
    contact_name = scrapy.Field()
    contact_phone = scrapy.Field()
    contact_email = scrapy.Field()
    valuation = scrapy.Field()
    release_time = scrapy.Field()
    address = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    id = scrapy.Field()

    category = scrapy.Field()
    trade_type = scrapy.Field()
    area = scrapy.Field()
    use_area = scrapy.Field()
    owner = scrapy.Field()
    located = scrapy.Field()
    use_type = scrapy.Field()

    pass
