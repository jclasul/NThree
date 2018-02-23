# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CarrefourItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Brand = scrapy.Field()
    Title = scrapy.Field()
    Price = scrapy.Field()
    IDnr = scrapy.Field()
    URL = scrapy.Field()
    Description = scrapy.Field()
    Kenmerken = scrapy.Field()
    image_url = scrapy.Field()
    #Currency = scrapy.Field()
    InStock = scrapy.Field()
    New = scrapy.Field()
    Alert = scrapy.Field()
    Field = scrapy.Field()

class GetUrls(scrapy.Item):
    URLS = scrapy.Field()