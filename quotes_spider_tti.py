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
    name = "tti"
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           ' Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,en-US;q=0.9,es;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'visid_incap_2587712=sgYkjh1BQuOEg4wcDLKoKntNr2MAAAAAQUIPAAAAAAD/qDLzMBFtxeyLFQDUseXx; cookieNecessary=true; cookiePerformance=true; cookiePersonalization=true; cookieMarketing=true; _pxvid=a4f5dd6e-8882-11ed-85be-5043497a4566; incap_ses_1433_2587712=qfzcaATiaW9e04NLLAvjE9L9tWMAAAAA/U/4J7Sa0lXmNTTumEJIrw==; check=true; renderid=rend01; _gid=GA1.2.659494663.1672871379; AMCVS_474027E253DB53E90A490D4E%40AdobeOrg=1; AMCV_474027E253DB53E90A490D4E%40AdobeOrg=1075005958%7CMCIDTS%7C19362%7CMCMID%7C02687671654111445180754236471124863841%7CMCAAMLH-1673476178%7C7%7CMCAAMB-1673476178%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1672878578s%7CNONE%7CMCSYNCSOP%7C411-19364%7CMCAID%7CNONE%7CvVersion%7C4.4.1; ln_or=eyIxMzEwMjUwIjoiZCJ9; s_cc=true; pxcts=469369ca-8c7f-11ed-a515-696f764f7068; s_sq=%5B%5BB%5D%5D; mbox=session#011e7a30b89440e880a089d9fc6ee603#1672874145|PC#011e7a30b89440e880a089d9fc6ee603.35_0#1736116179; _ga=GA1.1.200009707.1672433021; _ga_DZLYG7VYSV=GS1.1.1672871378.1.1.1672872417.0.0.0; _px3=7a9ad76a79acea017c3f5e7922d4074bd3191d51220324bce37f7cb697a71a5f:2148aaIclRe+AAOrWl3+xMbuuKj8CAGbk6JJL+dhFiHrPY8eDyxzsMsk+C0FCpV0kWKc5U5qXikjDanwGk7wnQ==:1000:VNYVIDdCiVc3Wny3kg/opGRPehwKRzbbevvl62Xj8Zk1XDMf/vFfbqe1ujtfdoFtlJXYDUVNrv+8Zu/MYhC1+sHpVcoWFiH66h5pqcJD4HIr4hnlvBybj/CQolnw/8VpcT0mMATVuoHRE43gABrkIeYIy2s+oD7ziKKUR2bC/QWLWlb1os/C0QOs4G9B0aSLbyLMazXa1qE66v3Vp9AVug==',
            'Host': 'www.tti.com',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        },
    }

    
    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.tti.com/content/ttiinc/en/apps/part-detail.html?partsNumber=%s' % partnumber]
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
        time.sleep(5)
        Inventory = self.driver.find_element(By.XPATH, "//*[contains(@id, 'ATS')]").text
        sku = self.driver.find_element(By.CSS_SELECTOR, "span[data-tti-partnum='%s']" % self.part_number).text
        orderAmount = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'col-xs-4 c-part-detail__pricing-quantity')]")
        pricesInfo = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'col-xs-4 c-part-detail__pricing-price')]")
        orderAmount.pop(0)
        pricesInfo.pop(0)
        data = []
        for i in orderAmount:
            quantity = i.text
            price = pricesInfo[orderAmount.index(i)].text
            data.append({'Distributor': 'onlinecomponents', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'})
        self.driver.close()
        self.driver.quit()
        print (data)


    