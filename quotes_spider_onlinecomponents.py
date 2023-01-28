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
    name = "onlinecomponents"
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.onlinecomponents.com/en/keywordsearch?text=%s' % partnumber]
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
            yield scrapy.Request(url=url,callback=self.parse_search_result)
           
            
    #the function checks if it is an exact match or not, if it is, it means that it is the only result, and it redirected to the product page, so we fetch the data from there, otherwise, we fetch the data from the search results page by selecting the exact match and entering the webpage, if there is no exact match, we return a dictionary with default values
    def parse_search_result(self, response):
        self.driver.get(response.url)
        time.sleep(3)
        Inventory = self.driver.find_element(By.XPATH, "//body/div/div/div/div/div/div/div/div/div/div[1]/div[1]/span[1]").text
        sku = self.driver.find_element(By.XPATH, "//*[contains(@class, 'text-uppercase text-olc-blue mb-0 text-center text-lg-left pt-10 SansSerifFontTitlePDP')]").text
        orderAmount = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'hdbreak')]")
        pricesInfo = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'col-4 text-right')]")
        pricesInfo.pop(0)
        data = []
        for i in orderAmount:
            quantity = i.text
            price = pricesInfo[orderAmount.index(i)].text
            data.append({'Distributor': 'onlinecomponents', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'})
        print (data)

    