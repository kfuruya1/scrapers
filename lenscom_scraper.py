import scrapy
#from scrapy.linkextractor import LinkExtractor
#from scrapy.spiders import Rule, CrawlSpider
#from lenscom_scraper.items import LenscomScraperItem


class LenscomScraperSpider(scrapy.Spider):
    #spider's name
    name = 'lenscom_scraper'

    #domains that are allowed
    allowed_domains = ['lens.com']

    #urls to start with
    start_urls = ['http://lens.com/contact-lenses/']

    def parse(self, response):
        for url in response.xpath('//a[contains(@href, "contact-lenses")]/@href').getall():
            print(url)
            yield scrapy.Request(response.urljoin(url), callback = self.parse_links)

    def parse_links(self, response):
        contacts = {}
        contacts['contacts'] = response.xpath('//div[@id="product_name"]/h1/text()').extract()
        contacts['size1'] = response.xpath('//span[@class="pack_count"]/text()').extract()
        contacts['size2'] = response.xpath('//span[@id="pack_details"]/text()').extract()
        contacts['price'] = response.xpath('//div[@id="product_pricing"]/div/h3/@data-base-price').extract()
        contacts['price2'] = response.xpath('//div[@id="product_pricing"]/div/div/div/h3/@data-base-price').extract()
        yield contacts




#the output file has a lot of empty rows because the spider tried to scrape pages like the rebate page which did not have relevant info
#so i just removed those rows in excel since i output to an excel file titled contacts.csv
#then sorted by contact name in alphabetical order




#        yield {
#            'contacts': response.xpath('//div[@id="product_name"]/h1/text()').extract(),
#            'size': response.xpath('/span[@class="pack_count"]/text()').extract(),
#            'price': response.xpath('/div[@class="save_914 save_display"]/text()').extract()
#            }

#        contacts = response.xpath('//div[@id="contacts_product_template"]/h1').extract()

    
    #telling the spider to extract all unique and canonicalized links, follow and parse them according to parse_items
#    rules = [
#        Rule(
#            LinkExtractor(
#                canonicalize = True,
#                unique = True
#                ),
#            follow = True,
#            callback = "parse_items"
#            )
#        ]

      
    #function to start the requests by going to all urls in start_urls
#    def start_requests(self):
#        for url in self.start_urls:
#            yield scrapy.Request(url, callback = self.parse, dont_filter = True)

    #how to parse items
#    def parse_items(self, response):
#        #list of items on the page
#        items = []
#        contacts = []
#        #only extract unique and canonicalized links
#        links = LinkExtractor(canonicalize = True, unique = True).extract_links(response)
#        #go through all found links
#        for links in links:
#            #check whether url domain is in allowed domains
#            is_allowed = False
#            for allowed_domain in self.allowed_domains:
#                if allowed_domain in link.url:
#                    is_allowed = True
#            #if allowed, create a new item and add to list of found items
#            if is_allowed:
#                if links not in items:
#                    item = LenscomScraperItem()
#                    item['url_from'] = response.url
#                    item['url_to'] = link.url
#                    items.append(item)
#                    for i in response.xpath('//div[@id="contacts_product_template"]'):
                        
        #return all found items
#        return items
