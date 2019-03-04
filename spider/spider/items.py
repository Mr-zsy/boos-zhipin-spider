# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    base = scrapy.Field()
    company = scrapy.Field()
    position = scrapy.Field()
    minPayment = scrapy.Field()
    maxPayment = scrapy.Field()
    eduBg = scrapy.Field()
    updateTime = scrapy.Field()
    updateMonth = scrapy.Field()
    kind = scrapy.Field()
    
