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

class QuotesSpider(scrapy.Spider):
    name = "alliedelec"
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.alliedelec.com/view/search?keyword=%s' % partnumber]
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
            yield scrapy.Request(url=url, callback=self.parse_search_result)    

##Pending to add the logic to check if the part number is in the search result or if it redirects you to the product page, if it redirects you to the product page then you need to call the parse_product_page function, if not then you need to call the parse_search_result function.
    def parse_search_result(self, response):
        self.driver.get(response.url)
        time.sleep(3)
        outOfStock = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'availability-text-full out-of-stock-message')]")
        if len(outOfStock) > 0:
            return {'Distributor': 'alliedelec', 'SKU': self.part_number, 'Inventory': 'out of stock', 'quantity': 'out of stock', 'price': 'out of stock', 'ClickUrl': response.url, 'currency': 'USD'}
        else:
            orderAmounts  = self.driver.find_elements(By.XPATH,"//*[contains(@class, 'new-material-available-standard-pricing-header-1')]") #this is the inventory amount to be ordered.
            pricesInfo = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'new-material-available-standard-pricing-header-2')]") #this is the price info it might contain different prices for different amount of products ordered
            sku = self.driver.find_element(By.XPATH, "/html[1]/body[1]/main[1]/div[1]/div[3]/div[3]/p[1]/strong[1]/span[1]")
            data = []
            Inventory = self.driver.find_element(By.XPATH,"/html[1]/body[1]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/p[2]").text
            orderAmounts.pop(0)
            pricesInfo.pop(0)
            for i in orderAmounts:
                quantity = i.text
                price = pricesInfo[orderAmounts.index(i)].text
                data.append({'Distributor': 'alliedelec', 'SKU': sku.text, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'})

        print (data)

    
        
  
     