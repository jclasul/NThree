# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TweedehandsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Brand = scrapy.Field()
    Title = scrapy.Field()
    Price = scrapy.Field()
    IDnr = scrapy.Field()
    URL = scrapy.Field()
    Place = scrapy.Field()
    Date = scrapy.Field()
    Author = scrapy.Field()
    Views = scrapy.Field()
    Description = scrapy.Field()
    Kenmerken = scrapy.Field()
    image_url = scrapy.Field()
    ActiveFrom = scrapy.Field()
    Author_id = scrapy.Field()
    Currency = scrapy.Field()