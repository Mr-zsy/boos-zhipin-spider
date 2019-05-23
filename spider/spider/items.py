# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #工作地点
    base = scrapy.Field()
    #公司名称
    company = scrapy.Field()
    #岗位名称
    position = scrapy.Field()
    #最低薪资
    minPayment = scrapy.Field()
    #最高薪资
    maxPayment = scrapy.Field()
    #学历背景
    eduBg = scrapy.Field()
    #更新时间
    updateTime = scrapy.Field()
    #更新月份
    updateMonth = scrapy.Field()
    #岗位类别
    kind = scrapy.Field()
    
