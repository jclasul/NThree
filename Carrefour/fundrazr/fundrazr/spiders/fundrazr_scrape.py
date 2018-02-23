import scrapy
from fundrazr.items import FundrazrItem

class Fundrazr(scrapy.Spider):
	name = "my_scraper"

	# First Start Url
	start_urls = ["https://fundrazr.com/find?category=Health"]
	npages = 2	

	# This mimics getting the pages using the next button. 
	for i in range(2, npages + 2):
		start_urls.append("https://fundrazr.com/find?category=Health&page="+str(i)+"")
	
	def parse(self, response):	
		yield scrapy.Request(start_urls, callback=self.parse_page1)	

		for href in response.xpath("//h2[contains(@class, 'title headline-font')]/a[contains(@class, 'campaign-link')]//@href"):
			# add the scheme, eg http://
			url  = "https:" + href.extract() 
			# for i in response.xpath('//*[@class="details tall"]'):
			# 	TESTCONTAINER = i.xpath('div//div[@class="stats-entry"]/p/text()').extract()[0]				
			# 	count += 1			
			yield scrapy.Request(url, callback=self.parse_page2)

	def parse_page1(self, response):
		item['main_url'] = response.url
		yield request

	def parse_page2(self, response):
		# Getting Campaign Title
		item['campaignTitle'] = response.xpath("//div[contains(@id, 'campaign-title')]/descendant::text()").extract()[0].strip()
		yield item

