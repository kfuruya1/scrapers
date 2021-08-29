import scrapy
import re

from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

a = 'https://www.1800contacts.com/lens/1-day-acuvue-trueye-90'
driver_options = webdriver.ChromeOptions()
driver_options.add_argument("--headless")
base_url = 'https://www.1800contacts.com/'
price_txt = ""

class X1800ScraperSpider(scrapy.Spider):
    name = 'x1800_scraper'
    allowed_domains = ['1800contacts.com']
#    start_urls = ['https://www.1800contacts.com/lens/frequency-55-aspheric']
    start_urls = ['http://1800contacts.com/lenses/view-all']

    def parse(self, response):
#        driver = webdriver.Chrome(options = driver_options)
#        driver.implicitly_wait(5)
        for url in response.xpath('//a[@class="product-link"]/@href').getall():
            full_url = base_url + url
#            driver.get(full_url)
#            driver.implicitly_wait(1)
#            price_element = driver.find_element_by_xpath('//span[@class="slashy ng-tns-c139-5"]')
#            price_txt = str(price_element.text)
#            selenium_response_text = driver.page_source
#            new_selector = Selector(text=selenium_response_text)
#            yield self.parse_links(new_selector)
            yield scrapy.Request(response.urljoin(full_url), callback = self.parse_links)
#        driver.close()


    def parse_links(self, response): #(self, response):
        contacts_18 = {}
#        driver = webdriver.Chrome(options = driver_options)
#        driver.implicitly_wait(5)
#        driver.get(response.url)
        if response.xpath('//p[contains(., "sad when your favorite")]/text()').get() is not None:
#            driver.close()
            print("discontinued")
            return
        if response.xpath('//h1[contains(., "Same as")]/text()').get() is not None:
#            driver.close()
            print("waste of time")
            return
        driver = webdriver.Chrome(options = driver_options)
        driver.implicitly_wait(5)
        driver.get(response.url)
#        driver.implicitly_wait(1)
#        contact_element = driver.find_element_by_xpath('//div[@class="aria-title sr-only"]')
#        contact_text = re.split('\|', contact_element.text)[0]
#        contact_18['contact'] = contact_text
#        print(contact_element)
#        print(contact_text)
        contacts_18['contact'] = response.xpath('//h1[@class="font-bold"]/text()').get()
#        <h1 _ngcontent-sga-c138="" class="font-bold">1-DAY ACUVUE TruEye
#        size_element = driver.find_element_by_xpath('//span[@class="lens-count ng-tns-c139-5 ng-star-inserted"]')
#        size_element = driver.find_element_by_xpath('//*[@id="pageWrapper"]/ctac-lens-product-detail-page/div/div/div/ctac-lens-product-detail/div/div/div/div[1]/ctac-slashy-price/div/div/span[4]')
#        size_text = size_element.text
#        contact_18['size'] = size_text
#        print(size_text)
        contacts_18['size'] = response.xpath('//div[contains(., "saline")]/text()').get()
#        contacts_18['size'] = response.xpath('//div[@class="row product-details ng-star-inserted"]/div[contains(., "lenses in")]/text()').get()

#        contacts_18['price'] = response.xpath('//*[@id="pageWrapper"]/ctac-lens-product-detail-page/div/div/div/ctac-lens-product-detail/div/div/div/div[1]/ctac-slashy-price/div/div/div/span/text()').get()
#        price_element = driver.find_element_by_xpath('//span[@class="slashy ng-tns-c139-5"]')
#        price_text= price_element.text
#//*[@id="pageWrapper"]/ctac-lens-product-detail-page/div/div/div/ctac-lens-product-detail/div/div/div/div[1]/ctac-slashy-price/div/div/div/span
#        contacts_18['price'] = response.xpath('//span[@class="slashy ng-tns-c139-5"]/text()').get()
#        contacts_18['price'] = (driver.find_element_by_xpath('//span[@class-"slashy ng-tns-c139-5"]')).text
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="pageWrapper"]/ctac-lens-product-detail-page/div/div/div/ctac-lens-product-detail/div/div/div/div[1]/ctac-slashy-price/div/div/div/span')))
        price_element = driver.find_element_by_xpath('//*[@id="pageWrapper"]/ctac-lens-product-detail-page/div/div/div/ctac-lens-product-detail/div/div/div/div[1]/ctac-slashy-price/div/div/div/span')
#        price_element = driver.find_element_by_xpath('//span[@class="slashy ng-tns-c139-5")]')
        price_text = price_element.text
        contacts_18['price'] = str(price_text)
#        contacts_18['price'] = (driver.find_element_by_xpath('//*[@id="pageWrapper"]/ctac-lens-product-detail-page/div/div/div/ctac-lens-product-detail/div/div/div/div[1]/ctac-slashy-price/div/div/div/span]')).text
#        print(price_element)
#        print(price_text)
        yield contacts_18
        driver.close()
#        print(response.xpath('//span[@class="slashy ng-tns-c139-5"]/text()').get())
