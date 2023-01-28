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
    name = "digikey"
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.digikey.com/']
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
        response = self.driver.execute_script("return fetch('https://www.digikey.com/suggestions/v3/search?keywordPrefix=%s&maxSuggestions=5', { headers: { 'site': 'US', 'lang': 'en', 'x-currency': 'USD' } }).then(response => { return response.json(); });" % self.part_number)        
    
        
  
        time.sleep(3)
        links = ['https://www.digikey.com' + response['suggestedProductNumbers'][0]['navigationUrl']] #this is the link to the product page, its a list of one element

        for link in links:
            
            yield scrapy.Request(url=link, callback=self.parse_product_page)
       
    def parse_product_page(self, response):
        fireFoxOptions = Options()  
        fireFoxOptions.add_argument("--headless") 
        fireFoxOptions.add_argument("--window-size=1920,1080")
        fireFoxOptions.add_argument('--start-maximized')
        fireFoxOptions.add_argument('--disable-gpu')
        fireFoxOptions.add_argument('--no-sandbox')
       # document.querySelector("div[data-testid='price-and-procure-title']")
        
        driver2 = webdriver.Firefox(options=fireFoxOptions, executable_path=r'../../geckodriver')
        
        driver2.get(response.url)
        time.sleep(3)
        inv = driver2.execute_script('price = document.querySelector("div[data-testid=\'price-and-procure-title\']"); return price;')
        time.sleep(3)
        inv = inv.text
        comp = driver2.execute_script('comp = document.querySelector("div[data-testid=\'qty-available-messages\'] div span"); return comp;')
        time.sleep(3)
        comp = comp.text
        time.sleep(3)
       
        Inventory = inv + comp
        sku = driver2.find_element(By.CSS_SELECTOR, "th[scope='col'] h1").text
        tables = driver2.find_elements(By.XPATH, "//tbody")
        infoprices = tables[4].find_elements(By.XPATH, "tr")
        quantity = 0
        data = []
        ## make for loop to infoprices to get all prices
        for i in infoprices:
            quantity = i.find_element(By.XPATH, "td[1]").text
            price = i.find_element(By.XPATH, "td[2]").text
            data.append({'Distributor': 'digikey', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'})



        print (data)