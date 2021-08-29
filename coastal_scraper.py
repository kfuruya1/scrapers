import scrapy
from scrapy import Selector
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
driver_options = webdriver.ChromeOptions()
#options.add_argument("--incognito")


count = 0
next_url = ['https://www.coastal.com/dwr/exec/refinedSearchAjaxController.viewAll.dwr']

class CoastalScraperSpider(scrapy.Spider):
    name = 'coastal_scraper'
    allowed_domains = ['coastal.com']
    start_urls = ['https://www.coastal.com/contactlenses#sorting=featuredAnywhere-asc&page=0&searchFamily=contacts&categoryCode=Contacts&filterGroup=&pdi_=[]&widgetExpanded=false&perfectFitExpanded=false&requestIdentifier=659190&hotSpotsEnabled=true&order=[]']
    
#https://www.coastal.com/dwr/exec/refinedSearchAjaxController.viewAll.dwr

#        'http://coastal.com/contact-lenses/']
#https://www.coastal.com/contactlenses#sorting=featuredAnywhere-asc&page=0&searchFamily=contacts&categoryCode=Contacts&filterGroup=&pdi_=[]&widgetExpanded=false&perfectFitExpanded=false&requestIdentifier=659190&hotSpotsEnabled=true&order=[]
    #count = 0

#    def scroll(driver, timeout):
#        #how long to wait before scrolling
#        scroll_pause_time = timeout
#        #find the height of the scroll
#        last_height = driver.execute_script("return document.body.scrollHeight")
#
#        while True:
#            #scroll to the bottom
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
##            #wait before scrollling again
#            time.sleep(scroll_pause_time)
#            #find new scroll height and see if it changed, i.e. if the page scrolled
#            new_height = driver.execute_script("return document.body.scrollHeight")
#            #if the heights are equal then it did not scroll so it's the bottom
#            if new_height == last_height:
#                break
#            last_height = new_height
    
    def parse(self, response):
#        for i in range(0, 3):
        driver = webdriver.Chrome(options=driver_options)
        driver.implicitly_wait(30)
        driver.get(response.url)
        last_height = driver.execute_script("return document.body.scrollHeight")
#        driver.switch_to.alert
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "close-reveal-newsletter")))
        driver.find_element_by_xpath('//span[@id="close-reveal-newsletter"]').click()
        timeout = 3
        element = driver.find_element_by_id("view-all-products")
#        last_height = driver.execute_script("return document.body.scrollHeight")
#        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#        time.sleep(timeout)
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID,"view-all-products")))
#                
        time.sleep(timeout)
        driver.find_element_by_xpath('//span[@id="view-all-products"]').click()
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        for i in range(0, 5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(timeout)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
                
#            except (TimeoutException, WebDriverException) as e:
#                break
#            #scroll to the bottom
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#            #wait before scrollling again
#            time.sleep(timeout)
#            #find new scroll height and see if it changed, i.e. if the page scrolled
#            new_height = driver.execute_script("return document.body.scrollHeight")
#            #if the heights are equal then it did not scroll so it's the bottom
#            if new_height == last_height:
#                break
#            last_height = new_height
        selenium_response = driver.page_source
        new_selector = Selector(text = selenium_response)
#        scroll(driver, 5)
#        for url in driver.find_element_by_xpath('//div[@class="product-tile-feature-image"]/a/@href'):
        for url in list(driver.find_elements_by_xpath('//div[@class="product-tile-feature-image"]/a')):
            link = url.get_attribute('href')
            print(link)
#            print(type(link))
            yield scrapy.Request(response.urljoin(link), callback = self.parse_links)
        driver.close()
            

        
#        for url in response.xpath('//div[@class="product-tile-feature-image"]/a/@href').getall():
#            print(url)
#            yield scrapy.Request(response.urljoin(url), callback = self.parse_links)



#            print(i)
#            yield scrapy.FormRequest(next_url, method="POST")
#            yield scrapy.Request(response.urljoin(next_url), callback = self.parse)

    def parse_links(self, response):
        contacts_c = {}
        contacts_c['contacts'] = response.xpath('//h1[@class="title-header-wrapper-red"]/text()').getall()
        contacts_c['size'] = response.xpath('//div[@class="title-header-packaging"]/p/text()').get()
        contacts_c['size2'] = response.xpath('//ul[@class="product-info-details-left-list"]/li/span[contains(., "lenses per box")]/text()').get()
        contacts_c['price'] = response.xpath('//span[@class="price-reg-on-sale"]/text()').get()
        contacts_c['price2'] = response.xpath('//span[@class="price-promo"]/text()').get()
        yield contacts_c

