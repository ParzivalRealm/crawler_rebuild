import scrapy
import ipdb
import os
import time

import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class QuotesSpider(scrapy.Spider):
    name = "plcity"
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):

        self.start_urls = ['https://www.plc-city.com/shop/en/content/search?q=%s' % partnumber]
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


    def parse_search_result(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        item = self.driver.find_element(By.CSS_SELECTOR, "#sniperfast_search .sniperfast_product a")
        links = [item.get_attribute('href')]
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_product_page)
       
    def parse_product_page(self, response):
        fireFoxOptions = Options()  
        fireFoxOptions.add_argument("--headless") 
        fireFoxOptions.add_argument("--window-size=1920,1080")
        fireFoxOptions.add_argument('--start-maximized')
        fireFoxOptions.add_argument('--disable-gpu')
        fireFoxOptions.add_argument('--no-sandbox')
        driver2 = webdriver.Firefox(options=fireFoxOptions, executable_path=r'../../geckodriver')
        driver2.get(response.url)



        name = driver2.find_element(By.XPATH, "//h1[contains(@itemprop,'name')]")
        inventoryelement = driver2.find_element(By.XPATH, "//div[contains(@class,'avilability_status')]")
        text = inventoryelement.text.rsplit(" ")
        inventory_amount = text[1]
        
        inventory_availability = text[0]
        price = driver2.find_element(By.XPATH, "//span[contains(@id,'new_price_display')]").text
        data = {'Distributor': 'plc-city', 'SKU': name.text, 'Inventory': inventory_availability, 'quantity': 1, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'}

        print (data)
       
