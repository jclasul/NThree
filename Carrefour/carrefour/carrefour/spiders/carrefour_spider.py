# -*- coding: utf-8 -*-
import scrapy
import re
from carrefour.IDnumbers import IDnumbers
from carrefour.items import CarrefourItem

class pagecounter:
    page_count = 1

    def pagecounter():
        pagecounter.page_count += 1

    def pagecounter_reset():
        pagecounter.page_count = 1

class CarrefourSpiderSpider(scrapy.Spider):
    name = 'carrefour_spider'
    writefiles = IDnumbers()
    start_urls = writefiles.GetFile(Mode='r', FileName = 'URLslist')[10:21]
   
    def parse(self, response):
        writefiles = IDnumbers()
        previous_values = writefiles.GetFile(Mode='r')
        CURRENT_PAGE = response
        # GET LIST of every ARTICLE on the page &
        # LOOP over every ARTICLE on the page
        articles = response.xpath('//div[@id="main-content"]/ul/li')
        for article in articles:
            # STORE response values 
            # THROUGH temp objects
            article_info = article.xpath('@data-product').extract_first() 
            '''
            article_json = json.loads(article_info)  # DICTIONARY approach , INCHES (") give problems 
            '''
            idnr = re.findall(r'\d\d\d\d\d\d\d\d',article_info)[0]
            # CALL predefined item class
            # STORE temp objects in scrapy item object 
            item = CarrefourItem()
            item['IDnr'] = idnr

            # CHECK for IDnr in scraped LIST
            if previous_values is not None:
                if idnr not in previous_values:
                    # GET Next URL (=article's description page)
                    # GOTO next url &
                    # RUN parser for next url
                    writefiles.GetFile(Mode="a", WriteString = idnr)
                    print('\n\t New ID-NR \t', idnr)
                    NURL = article.xpath('div//h2/a/@href').extract_first()
                    res = scrapy.Request(url =  response.urljoin(NURL), callback=self.parseProduct)
                    ##print('\t going to next URL', response.urljoin(NURL))
                    item['URL'] = NURL
                    res.meta['item'] = item
                    yield res
                        # TESTING ONLY
                    #return
                        #
                else:
                    pass
            else:
                writefiles.GetFile(Mode="a", WriteString = idnr)

        # GET next page &
        # RERUN this parse until None        
        next_page = CURRENT_PAGE.xpath('//ul/li[@class="next"]/a/@href').extract_first()
        print(pagecounter.page_count, '\t\t', next_page)
        if int(re.findall(r'\d+', next_page)[-1]) < 7 and next_page is not None:
            pagecounter.pagecounter()
            yield response.follow(next_page, callback=self.parse)       

    def parseProduct(self, response):
        # GET items passed from first-url
        item = response.meta['item']
        # THROUGH temp objects
        #
        brand = response.xpath('//div/h2[@class="brand-name"]/text()').extract_first().strip()
        price = response.xpath('//div[@class="current-price"]/@content').extract_first()
        title = response.xpath('//div/h1[@class="product-name"]/text()').extract_first().strip()
        instock = response.xpath('//div[@class="promos"]/p/text()').extract_first()
        imgurl = response.xpath('//div[@id="content"]//img/@src').extract_first()
        itemnew = response.xpath('//div//span[@class="alert new"]/a/text()').extract_first()
        alert = response.xpath('//span[@class="top"]/a/text()').extract()
        fields = response.xpath('//nav/div/ul/li/a/span/text()').extract()

        case_dict_fields = {}
        for i, field in enumerate(fields):
            indv_field_name = 'CAT_' + str(i)
            indv_field_val = field

            newdict = {indv_field_name : indv_field_val}
            case_dict_fields.update(newdict)         

        # SPECIAL CASE :: KENMERKEN
        kenmerken = response.xpath('//div[@id="product-keypoints"]')
        # APPEND kenmerken to LIST in FOR loop
        case_dict_kenmerken = {}  
        # optioncnt = 1
        for kenmerk in kenmerken.xpath('//div/table//td[@class="title"]'):
            # GET name and value for each kenmerk,
            # POSSIBLE to have and GET multiple kenmerken (e.g. for options)
            indv_kenmerk_value_STD = kenmerk.xpath('following-sibling::td/text()').extract_first().strip().split()
            indv_kenmerk_value_BIN = kenmerk.xpath('following-sibling::td/span/@class').extract_first()
            indv_kenmerk_naam = kenmerk.xpath('./text()').extract_first().strip()

            if indv_kenmerk_value_BIN is None:
                indv_kenmerk_val = indv_kenmerk_value_STD
            else:
                indv_kenmerk_val = indv_kenmerk_value_BIN            

            newdict = {indv_kenmerk_naam : indv_kenmerk_val}
            case_dict_kenmerken.update(newdict)  

        item['Price'] = price
        item['Brand'] = brand
        item['Title'] = title
        item['InStock'] = instock
        item['image_url'] = imgurl
        item['New'] = itemnew
        item['Alert'] = alert       
        item['Kenmerken'] = case_dict_kenmerken   
        item['Field'] = case_dict_fields           

        yield item 

''' 
            if 'Opties' in indv_kenmerk_naam:
                # indv_kenmerk_naam = indv_kenmerk_naam + str(optioncnt)
                # optioncnt += 1
                option_list.append(indv_kenmerk_val)   
            # ADD combination name and value to dictionary &
            # APPEND dictionary to temp list
            ##newdict = {'Opties' : option_list}
            ##case_dict.update(newdict)    

        date = response.xpath('//span[@class="views-since"]/time/@datetime').extract_first()
        views = response.xpath('//span[@class="views-count"]/text()').extract_first()        
        place = response.xpath('//section/ul/li/@data-seller-map-location').extract_first()
        activefrom = response.xpath('//section/ul/li/span[@class="data-text"]/text()').extract_first()
        author_id = response.xpath('//section/div/a[@class="seller-name"]/@href').extract_first().strip("/profiel/")
        # USE next sibling to get description and items
        description = response.xpath('//h2/following-sibling::p/text()').extract()
        # SPECIAL CASE :: KENMERKEN
        kenmerken = response.xpath('//h2/following-sibling::dl')
        # APPEND kenmerken to LIST in FOR loop
        case_dict = {}  
        # optioncnt = 1
        option_list = []
        for kenmerk in kenmerken.xpath('dd'):
            # GET name and value for each kenmerk,
            # POSSIBLE to have and GET multiple kenmerken (e.g. for options)
            indv_kenmerk_naam = kenmerk.xpath('preceding::dt[position()<2]/text()').extract_first().strip(':')            
            indv_kenmerk_val = kenmerk.xpath('./text()').extract_first().replace(',','').strip()

            if 'Opties' in indv_kenmerk_naam:
                # indv_kenmerk_naam = indv_kenmerk_naam + str(optioncnt)
                # optioncnt += 1
                option_list.append(indv_kenmerk_val)   
            # ADD combination name and value to dictionary &
            # APPEND dictionary to temp list
            newdict = {indv_kenmerk_naam : indv_kenmerk_val}
            case_dict.update(newdict)
            
        newdict = {'Opties' : option_list}
        case_dict.update(newdict)    
        item['Kenmerken'] = case_dict
            #case_list.append(newdict)
            #item['Kenmerken'] = newdict

        # STORE temp objects in scrapy item object 
        item['Title'] = title
        if len(price) == 1 or price[0] == 'Prijs':
            item['Currency'] = None
            item['Price'] = None
        else:
            item['Currency'] = price[0]
            item['Price'] = int(price[-1].split(',')[0].replace('.',''))
            
        item['Brand'] = brand
        item['Date'] = date
        item['Views'] = views        
        item['Place'] = place
        item['Description'] = description
        item['ActiveFrom'] = activefrom
        item['Author_id'] = author_id
        item['InStock'] = instock

        # IMAGES PARSER
        # to-do different parser ? parseImg ?
        # # #
        img_list = []
        for img in response.xpath('//img/@src').extract():
            if img.startswith('https://img.2dehands.be/f/normal/'):
                img_list.append(img)

        item['image_url'] = img_list
        # YIELD to write as JSON/CSV/...  
        yield item '''