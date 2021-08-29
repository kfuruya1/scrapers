import scrapy
import re

page = 1
base_url = "https://lenscrafters.com/lc-us/contact-lenses"

class LcScraperSpider(scrapy.Spider):
    name = 'lc_scraper'
    allowed_domains = ['lenscrafters.com']
    start_urls = ['https://lenscrafters.com/lc-us/contact-lenses']
#    page = 1
#    base_url = "http://lensecrafters.com/lc-us/contact-lenses"



#<a class="nextPageNumerical total-pages"
#    onclick="goToURL('https://www.lenscrafters.com/lc-us/contact-lenses?page=5')">
#    5
#</a>

    def parse(self, response):
        total_pages = response.xpath('//a[@class="nextPageNumerical total-pages"]/text()').get()
        pages = int(total_pages)
        for i in range(0, pages):
            if i == 0:
                print(base_url)
                yield scrapy.Request(response.urljoin(base_url), callback = self.parse_links)
            else:
                page_num = i + 1
                next_url = base_url + "?page=" + str(page_num)
                print(next_url)
                yield scrapy.Request(response.urljoin(next_url), callback = self.parse_links)

    def parse_links(self, response):
        for url in response.xpath('//div[@class="names"]/a/@href').getall():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_items)

    def parse_items(self, response):
        contacts_lc = {}
        contacts_lc['contact'] = response.xpath('//h1[@class="contact-lens-name"]/text()').get()
        contacts_lc['size'] = response.xpath('//div[@class="lenses-per-box"]/text()').get()
        contacts_lc['price'] = response.xpath('//span[@class="box-list-price"]/text()').get()
        yield contacts_lc



#so i wanted to originally just srape all the info from the pages containing all of the contacts
#without having to navigate to each link for each contact lens but the overview pages do not have
#the sizes for all of the contacts in the names which is where i was getting the size from
#so i was forced to still go to each individual link and scrape from each page
#BUT there are errors on the website where the size is listed as 0 instead of 90 or 30 so those need to be fixed
        




#parts of the code below work but once i realized that not all of the sizes were there i stopped working on it

##        contacts_lc = {}
##        temp =(response.xpath('//span[@class="brand-name"]/text()').getall())
#        print(temp[1])
#        print([a.split('30 |6 |90', 1) for a in temp])
#        contacts_lc['contact'] = [a.split('3|6|9', 1)[0] for a in temp]
#        contacts_lc['size'] = [b.split('3|6|9', 1)[1] for b in temp]
#        contacts_lc['contact'] = response.xpath('//span[@class="brand-name"]/text()').getall()
#        contacts_lc['price'] = response.xpath('//span[@class="box-offer-price"]/text()').getall()
#        yield contacts_lc
##        temp2 = (response.xpath('//span[@class="box-offer-price"]/text()').getall())
##        count = 0
##        for i in temp:
#            contacts_lc['contact'] = re.split('3|6|9', i)[0]
#            contacts_lc['size'] = re.split('3|6|9', i)[1]
#            contacts_lc['price'] = temp2[count]
#            count += 1
#            yield contacts_lc
##            print(re.split('(30|6|90)', i)[1]) # + re.split('3|6|9', i)[1])           
