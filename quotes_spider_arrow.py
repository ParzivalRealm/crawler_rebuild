import scrapy
import ipdb
import os
import time
import re
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
## Pending work, they have an API, they don't allow scraping, so we need to use the API to get the data, and then we need to use selenium to get the data from the product page, and then we need to use selenium to get the data from the search results page
class QuotesSpider(scrapy.Spider):
    name = "arrow"
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.arrow.com']
        self.part_number = partnumber
        fireFoxOptions = Options()  
        fireFoxOptions.add_argument("--headless") 
        fireFoxOptions.add_argument("--window-size=1920,1080")
        fireFoxOptions.add_argument('--start-maximized')
        fireFoxOptions.add_argument('--disable-gpu')
        fireFoxOptions.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(options=fireFoxOptions, executable_path=r'../../geckodriver')


    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies= {':authority': 'www.arrow.com', ':method': 'GET', ':path':'/','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding':'gzip, deflate, br','accept-language':'en-US,en;q=0.9','cache-control':'max-age=0'},callback=self.parse_search_result)
           
            
    #the function checks if it is an exact match or not, if it is, it means that it is the only result, and it redirected to the product page, so we fetch the data from there, otherwise, we fetch the data from the search results page by selecting the exact match and entering the webpage, if there is no exact match, we return a dictionary with default values
    def parse_search_result(self, response):
        ipdb.set_trace()
        self.driver.get(response.url)
        search_url = 'https://www.arrow.com/en/products/search?cat=&q=%s&r=true' % self.part_number
        ipdb.set_trace()
        yield scrapy.Request(url=search_url, callback=self.parse_product_page)
    ##arrow,allie,mouser are the same?
    def parse_product_page(self, response):
        ipdb.set_trace()
    #     self.driver.get(response.url)
    #     data = {}
    #     exactMatch = False
    #     if response.url == 'https://www.arrow.com/en/products/search?cat=&q=%s&r=true' % self.part_number:
    #         ipdb.set_trace()
    #         exactMatch = False
    #     else:
    #         ipdb.set_trace()
    #         exactMatch = True
    #     if exactMatch:
    #         ipdb.set_trace()
    #         Inventory = self.driver.find_element(By.XPATH, "//*[contains(@class, 'BuyingOptions-title BuyingOptions-title--underlined ng-star-inserted')]").text
    #         sku = self.driver.find_element(By.XPATH, "//div[@name='product-details']//section//section//div//div//div//div//div//div//div//div//span[contains(text(),'%s')]" % self.part_number)
    #         price = self.driver.find_element(By.XPATH, "//*[contains(@class, 'BuyingOptions-priceTiers-price ng-star-inserted')]").text
    #         quantity = self.driver.find_element(By.XPATH, "//*[contains(@class, 'BuyingOptions-priceTiers-quantity ng-star-inserted')]").text
    #         data = {'Distributor': 'arrow', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'}
    #         return data
    #     else:
    #         ipdb.set_trace()
    #         links = self.driver.find_element(By.XPATH, "//*[contains(@data-part-name, '%s')]" % self.part_number)
    #         if links:
    #                 yield scrapy.Request(url=links.get_attribute('href'), callback=self.parse_product_page)
    #         else:
    #             data = {'Distributor': 'arrow', 'SKU': 'no match', 'Inventory': '0', 'quantity': '0', 'price': '0', 'ClickUrl': 'no match', 'currency': 'USD'}
    #             return data

    # def parse_product_page(self, response):
    #     ipdb.set_trace()
    #     self.driver.get(response.url)
    #     Inventory = self.driver.find_element(By.XPATH, "//*[contains(@class, 'BuyingOptions-title BuyingOptions-title--underlined ng-star-inserted')]").text
    #     sku = self.driver.find_element(By.XPATH, "//div[@name='product-details']//section//section//div//div//div//div//div//div//div//div//span[contains(text(),'%s')]" % self.part_number)
    #     price = self.driver.find_element(By.XPATH, "//*[contains(@class, 'BuyingOptions-priceTiers-price ng-star-inserted')]").text
    #     quantity = self.driver.find_element(By.XPATH, "//*[contains(@class, 'BuyingOptions-priceTiers-quantity ng-star-inserted')]").text
    #     data = {'Distributor': 'arrow', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'}
    #     return data
    
        
  
     