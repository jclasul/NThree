import scrapy
from tweedehands.items import TweedehandsItem
from tweedehands.IDnumbers import IDnumbers

class pagecounter:
    page_count = 1

    def pagecounter():
        pagecounter.page_count += 1
        return pagecounter.page_count


class tweedehands_spider(scrapy.Spider):    
    name = "tweedehands"
    allowed_domains = ['2dehands.be']
    start_urls = [
        'https://www.2dehands.be/motoren/?language=nl&language=fr&p=nl&p=be&p=fr',
    ]

    def parse(self, response):
        writefiles = IDnumbers()
        previous_values = writefiles.GetFile(Mode='r')
        CURRENT_PAGE = response
        # GET LIST of every ARTICLE on the page &
        # LOOP over every ARTICLE on the page
        articles = response.xpath('//article')        
        for article in articles:
            # STORE response values 
            # THROUGH temp objects
            idnr = article.xpath('@id').extract_first()

            # CALL predefined item class
            # STORE temp objects in scrapy item object 
            item = TweedehandsItem()
            item['IDnr'] = idnr

            # CHECK for IDnr in scraped LIST
            if previous_values is not None:
                if idnr not in previous_values:
                    # GET Next URL (=article's description page)
                    # GOTO next url &
                    # RUN parser for next url
                    writefiles.GetFile(Mode="a", WriteString = idnr)
                    print('\t New ID-NR \t', idnr)
                    NURL = article.xpath('div/@data-adv-link').extract_first()
                    res = scrapy.Request(url =  response.urljoin(NURL), callback=self.parseProduct)
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
        next_page = CURRENT_PAGE.xpath('//nav/a[@rel="next"]/@href').extract_first()
        print(pagecounter.page_count, '\t\t', next_page)
        if next_page is not None:
            pagecounter.pagecounter()
            yield response.follow(next_page, callback=self.parse)            

    def parseProduct(self, response):
        # GET items passed from first-url
        item = response.meta['item']
        # THROUGH temp objects       
        title = response.xpath('//section[@class="panel-content"]//h1/text()').extract_first().strip()
        price = response.xpath('//span[@class="price"]/text()').extract_first().strip().split()
        date = response.xpath('//span[@class="views-since"]/time/@datetime').extract_first()
        views = response.xpath('//span[@class="views-count"]/text()').extract_first()
        author = response.xpath('//span[@class="name"]/text()').extract_first().strip()
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
            
        item['Date'] = date
        item['Views'] = views
        item['Author'] = author
        item['Place'] = place
        item['Description'] = description
        item['ActiveFrom'] = activefrom
        item['Author_id'] = author_id

        # IMAGES PARSER
        # to-do different parser ? parseImg ?
        # # #
        img_list = []
        for img in response.xpath('//img/@src').extract():
            if img.startswith('https://img.2dehands.be/f/normal/'):
                img_list.append(img)

        item['image_url'] = img_list
        # YIELD to write as JSON/CSV/...
        yield item 