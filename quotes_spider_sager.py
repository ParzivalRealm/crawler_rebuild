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
    name = "sager"
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.sager.com',
            'method': 'GET',
            'path': '/search/?Keywords=2904602',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en,en-US;q=0.9,es;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'visid_incap_2582790=vaMQXV0CT62q+4dAtDViGd1Nr2MAAAAAQUIPAAAAAABRY2XxLXNeHPH8rmtgNsyL; ASP.NET_SessionId=ircnhgz100zljmi5pnpsvwvm; UserInfo=UserID=ui0+pqRaGvPBlVKhhqaxdcMSe5/hLnJhJDfUhK1w5YqmzTBGBrDbfQ==; nlbi_2582790=T+sRLHRbeQYHrS0eLM31jAAAAADgskGQkXE8I3uAGOAYHiC9; incap_ses_1434_2582790=cBuCXeoWh3yHZMXvqpjmExRGt2MAAAAAkM0m3p0fA8ggr0WHSumFzw==; _gid=GA1.2.187680922.1672955413; _gat_gtag_UA_20538038_1=1; _gat_gtag_UA_20538038_6=1; _ga_B3M4VRJJ3Z=GS1.1.1672955413.2.0.1672955413.0.0.0; _ga=GA1.1.1716018081.1672433119; _ga_24387CKKR0=GS1.1.1672955413.2.0.1672955413.60.0.0; _hjSessionUser_1750735=eyJpZCI6ImU4N2MyZDViLTRkMjYtNTE5My1hM2U2LWE1MDU2MjRlMDM4YyIsImNyZWF0ZWQiOjE2NzI0MzMxMTkwMjEsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample=0; _hjSession_1750735=eyJpZCI6ImY4YzVkYmZlLWMwZDktNDRmMC05ZjkzLWZmMDYzMDFlYTkyOCIsImNyZWF0ZWQiOjE2NzI5NTU0MTM5MTcsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; nlbi_2582790_2147483392=w/ecRlcooVj376ZlLM31jAAAAACmU1X8SYsg1UL7dXhj3+ck; reese84=3:iTXmz2McSHOkVmH1yPLpLA==:gWxSCt/oQWvlUmlvTx8wr2VItQZ13ZmmvSy8t9YZ53LSHFzLrrrHifEBLaH6DA/U+V79aNE+LKp8lKOkHh6dy4d7Y3k3EZWzzPk+j/67oL6W9EJl4PyljyuyDos6A3ciQA2UW0MFqVEf2YSymHAF29xB62juXf6vUMwJ7FGU2WxD/6RGCB32X61RewwGlhETGQ99Mi2VPLKWI6BLXiF1qncW11+1qUx+cold5QGhuAlMNfu2YN5D6HToBOvjUc6sThFdPNv0FWWh2GJajvnQPqVzg5apDvIzvnyMPEOKUV3PJEmCcduXiCvwyQwoZ/ahbS3QAASc6qRaD3a7notiIpfP3HrJiZDT0TlTRknwhEviLw/FQTOb5aYFw1FOAHJLksV0uKtLJcEA42Nc9Xez5eQogcXiQsNzh3wo5kMOquz/k0hAhzerfhd7u3OC0oxP6whqlhIBtxmNyz4U6popxzNdgOQR9XfTgN+HLZPjGGM=:4TxkohrstWN0sVdpb8UUUopMF53bXzxoEh2CZxwueiw=',
            'pragma': 'no-cache',
            'referer': 'https://www.sager.com/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
    }


    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.sager.com/search/?Keywords=%s' % partnumber]
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
           
            
    def parse_search_result(self, response):
        self.driver.get(response.url)
        time.sleep(3)
        sku = self.part_number
        data = []
        infoTables = self.driver.find_elements(By.XPATH, "//table[contains(@class,'Pricing')]")
        Inventory = infoTables[1].find_element(By.XPATH, "tbody/tr").text
        pricingTable = infoTables[0].find_elements(By.XPATH, "tbody/tr")
        for i in pricingTable:
            #split by : to get the quantity and price
            separatedInfo = i.text.split(':')
            quantity = separatedInfo[0]
            price = separatedInfo[1]
            data.append({'Distributor': 'onlinecomponents', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'})

        print (data)


    