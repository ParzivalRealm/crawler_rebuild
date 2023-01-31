import scrapy
import ipdb
import os
import time

import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
##ipdb.set_trace()
class QuotesSpider(scrapy.Spider):
    name = "wiautomation"
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://us.wiautomation.com/search?q=%s' % partnumber]
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
        time.sleep(3)
        item = self.driver.find_element(By.CSS_SELECTOR, "a.product_name") # debe de revisar si en el search result viene alguna descripcion que contenga exactamente el part_number
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
        name = driver2.find_element(By.XPATH, "//*[contains(@class,'wrap_main_content_global')]")
        text = name.text
        arr = text.rsplit("\n")
        url = response.url

        print({'Distributor': 'wiautomation', 'SKU': arr[21], 'Inventory': arr[23], 'quantity': 1, 'price': arr[24], 'ClickUrl': url, 'currency': 'USD' })
      
