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
    name = "mrosupply"


    start_urls = [
        
    ]

    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.mrosupply.com/search_spring/?q=%s' % partnumber]
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

    def parse_search_result(self, response):
        self.driver.get(response.url)
        Match = self.driver.find_element(By.XPATH, "//div[contains(@class,'m-catalogue-product-img')]")
        if Match:
            links = [Match.find_element(By.XPATH, "a").get_attribute('href')]
        else:
            links = []
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_product_page)

    def parse_product_page(self, response):
        self.driver.get(response.url)
        time.sleep(3)
        availabilityFlag = self.driver.find_element(By.XPATH, "//*[contains(@class,'u-warning')]")
        availabilityFlag = availabilityFlag.text
        data = []
        if availabilityFlag == 'CONFIRM AVAILABILITY':
            availability = '0'
            data.append ({"Distributor":"mrosupply","SKU":self.part_number, "Inventory": availability, "quantity": 1, "price": "na", "ClickUrl": response.url, "currency": "USD"})
            
        else:
            availability = availabilityFlag
            price = self.driver.find_element(By.XPATH, "//div[contains(@class,'productDetail--card--pricing')]/div/p[contains(@class,'price')]")
            price = price.text
            sku = self.part_number
            data.append ({"Distributor":"mrosupply","SKU":sku, "Inventory": availability, "quantity": 1, "price": price, "ClickUrl": response.url, "currency": "USD"})
           
        self.driver.close()
        self.driver.quit()
        print(data)