import scrapy


class LensdirectScraperSpider(scrapy.Spider):
    name = 'lensdirect_scraper'
    allowed_domains = ['lensdirect.com']
    start_urls = ['http://lensdirect.com/contact-lenses', 'https://www.lensdirect.com/contact-lenses?page=2']
#https://www.lensdirect.com/contact-lenses?page=2

    def parse(self, response):
        for url in response.xpath('//div[@class="app-search-results-container"]/a/@href').getall():
            full_url = "http://lensdirect.com" + url
            yield scrapy.Request(response.urljoin(full_url), callback = self.parse_links)
            
    def parse_links(self, response):
        contacts_d = {}
        contacts_d['contacs'] = response.xpath('//div[@class="product-name-wrapper main-product-title"]/h1/text()').extract()
#        contacts_d['contacts'] = response.xpath('//div[@class="product-name"]/text()').extract()
        contacts_d['size'] = response.xpath('//li[contains(.,"Lens Per Box")]/text()').extract()
        contacts_d['price'] = response.xpath('//div[@class="price-tier"]/div/div[@class="price"]/text()').extract_first()
        yield contacts_d


#theres no real consistent way that this website indicates the number of lenses in each box
#this code only gets the ones that follow some semblance of a pattern
#the rest are just buried in a wall of text after a lot of fluff product description or only in the name of the product and not in the description
#these instances are all instances where either the size is in the name of the product
#or it's going to be a 6 pack

