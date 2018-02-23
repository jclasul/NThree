# -*- coding: utf-8 -*-
import scrapy
from carrefour.items import GetUrls
from carrefour.IDnumbers import IDnumbers

class GeturlsSpider(scrapy.Spider):
    name = 'GetUrls'
    start_urls = ['https://webshop.carrefour.eu/nl/']

    def parse_item(self, response):
        writefiles = IDnumbers()
        #item = GetUrls()
        previous_values = writefiles.GetFile(Mode='r', FileName = 'URLslist')

        urllist = []      

        hrefs = response.xpath('//div/ul/li/a/@href')
        for href in hrefs.extract():
            if href.startswith('/nl/') and len(href.split('/')) > 4:
                writefiles.GetFile(Mode='a', FileName = 'URLslist', WriteString = response.urljoin(href))
                urllist.append(href)
        
        item['URLS'] = urllist

        yield item