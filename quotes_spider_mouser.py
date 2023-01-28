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
    name = "mouser"
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.mouser.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en,en-US;q=0.9,es;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'CARTCOOKIEUUID=f1d56413-d95d-490c-bf95-64db0d611038; __neoui=f0d07519-2b49-490c-9d8f-b45eafc6093a; _gcl_au=1.1.2067885275.1669681876; _pxvid=2292b021-6f7d-11ed-8c09-754b4f6f4577; sa-user-id=s%253A0-4cf2ca78-7117-4e85-7923-bfd3c2bcfa20.ZWs%252Fbz7Fc5n0lYUDJt%252FaNeibn98IcjUyfaDBydWYSJg; sa-user-id-v2=s%253ATPLKeHEXToV5I7_Twrz6ILu9pFI.rLVbCglqL2LUtvonR6FiDNFusGJ40hZXP6Eh%252FleOV5c; LPVID=M1ZmRhZmQ2OTU4ODFhNzUz; ASP.NET_SessionId=12uqme4ocdgc20av11zlw15d; akacd_Default_PR=3850413654~rv=37~id=e11f740bf9c11d480828c12b1e005a1a; ln_or=eyIxNDExNzIyIjoiZCJ9; rbuid=rbos-c883b87d-8cc7-47a0-8c04-dd72e106eaf4; _gid=GA1.2.1750528604.1672960860; pxcts=9e33f005-8d4f-11ed-983a-795550647a4d; __RequestVerificationToken=i6R9Oiza82aRcwOA7ovMIQTG1mEyzRFdiM6hqvqJIQXItPf18OkFT_0E3tXr65KNI4x-LT2msvlMH9EO49QKqYlnTYo1; bm_sz=8FD5A8B307EB0ADC4A72EAED0F9044B4~YAAQRrU7F5+9HjeFAQAAJsL5iBL5UI2naKB1n/CBz4Q3tav8vlSf/WIPH+SFXTdsa3+/mQ0oljxUl3Eg9RcnTNgfmzM/ICkvxz8bF1SFL78JqoO8A2IMU6sPL6t9rqcdschBzCiJE3MscWz/gIYn1Vgv1LYeFrLdLL7HxSPjKZ1vcJXHjyN1id3bRfLmFz6wsT2u0+23NxqkJyUZmEt825jfC/IN+K31HXFiIqyhhBVdN3xghsw6B+A8HF+qoFPdp1HHVXYcJ3PxRXVPugSRR29pnF1Mqos2qY4BJr4/0n4BtYk=~4600131~3621425; fs_uid=#Z1BBJ#5205605897097216:5018141469659136:::#/1701217876; LPSID-12757882=CN05csgPRYm7j_V3dHWbVg; AKA_A2=A; bm_mi=45C89A70560ADB706C9819D0CBBD64B4~YAAQi7U7F7N4tYaFAQAAYxn8iBLlfkawepsYgCCYlPTjkW54OINi1wSbCEFEV1J9a2bntAwJLZf4EFJfBvgX4oYMHjidGLw6glLJgHLBrkHL/Dytc9IbfjARTUmgBvxGzq4VIsQgPtQYqDeXcIb5Ugd7N8A2z6yvlx0TyPzlxUQdRx6L9tD9yPSzg/yI+Hmnbn0BV25ya3tXwNJteWBM6+3rrusZfbsZXMBmWKxoxFFRBX/QbNCICtgsGouRJNuJsIwP46Lr4jtNHgBEg/jBEXivG3pqzikJlvVC1WO8MtGH2ksq+6/ySExrrdYT9A==~1; ak_bmsc=2F8369AEB5CC3AA941E043FF30B5DDDE~000000000000000000000000000000~YAAQi7U7F816tYaFAQAAfiP8iBLw6lffHOmWWDhzulym2wQB6O3QhO9B291SSJfpevdtqhKR8dJF8W20Lo2ZQBU///Hu5pfWrsXupTM3oTnmrFtnTNBbQ8YJgnHZ839eHheQxMO+4bSD+PERjobmkH4uFi0AGQFiOvmGcEQs39GbB/T6bNpf1mtjmvqwjvWVxi1Qst9pMeSfRPGy6aLubR+ZKALeonKwcmErw7mf2F0OiT8WKDtfiLVv5CwOL0Bub25fw7HJwFFeWBwZc9mBvgg/olNvGhT60xTRRqy3EF3O1vYXLb4EDOZcFXvCNVmqgz3+n67UB9GtD6zsS7XId83kgmF7TqaMh9B4LGYE0YUVMbeagkf+EbtUkmF98XkZEwkJx7BpEZqQ70T2qqKSNqOt8jrVOHtb1GEltZM=; preferences=ps=&pl=en-US&pc_www=USDu; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jan+06+2023+15%3A33%3A13+GMT-0600+(Central+Standard+Time)&version=6.37.0&hosts=&consentId=d9b90995-8955-4c17-ad1e-3bcb81aed607&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=MX%3BNLE; OptanonAlertBoxClosed=2023-01-06T21:33:13.685Z; _ga_1KQLCYKRX3=GS1.1.1673040348.3.1.1673040793.56.0.0; _ga=GA1.1.405975305.1669681876; QSI_HistorySession=https%3A%2F%2Fwww.mouser.com%2F~1672960890838%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D294602~1672961470381%7Chttps%3A%2F%2Fwww.mouser.com%2F~1673040507458%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D294602~1673040510384%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D2904602~1673040537099%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D6SL32105BE211UV0~1673040684427%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D2904602~1673040688763%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D6SL32105BE211UV0~1673040791347%7Chttps%3A%2F%2Fwww.mouser.com%2Fc%2F%3Fq%3D2904602~1673040795208; _px3=97325e2a2f19f8495a4a74d7704b19da81d580407793ed1f96da50870fbfbe9c:275+7m7erYvCP/KFMH0gzi+8J9Ukq5q7oP6q6551wpjC/Zk67l/kWivmoUE1I7TLMB+lEZb01EbAUsEEUibZdQ==:1000:b6/p0OfvyTqHHGQuPpM1IdFIJpYSYaTGTsXghPY6z0R2gxC5RjdmCzxEOQ4aSbZU3zd8jOedBQ1G6wVaY9I/R590IYv8dh7AYTFTqQoJEQjS86aQGijdAaZ+TEeaPW83wncesl8kZWcnTd6fK+I019niYGGnMNoA5TOb7ZIOpmWBoiMyivGnARRge4GIcWCv3HYZgUpY1Krvvtzr6p4+Ug==; _abck=CAF140CCDE7863E78630E61C51D0FF48~-1~YAAQi7U7F9f5toaFAQAAXqsDiQmlQQ+wSQDLr9WhJjJsRUAAdY+43REFqrhrgvSAJdYROHLPtMzYJDnsaI3KMGxBP6H4iGZQDOm0/8YZiBqV/qxw51QWpHxjR3OgJDf+vpOn48u5ohrzEIArRIkO7m/819RUXgmfXdU/UFLrqrm/YUWBIOHXsshAENs56Xio7PPSFYMPqMyrhxa5gNwRYvLBF+Mh3+C8rz6ojOxzCe8JRUveril+H6F0JzHDtG8p0EvI47+Zy3iDxoX8bLS4zrougJUQ11rlAztC4t8Na+AkOxckMKAFY9TMZWVIMi2vvM6hBgP8MGXyEifm6/S2JUR46BRz1DwP3XjFdd+uOg+jpBcbIRkwCaWu4IzROA9TX1CEF7s8xkZEueE5HPOt0rAhdZOBycqzZxGZW4PgjV3BXzen~-1~-1~-1; _ga_15W4STQT4T=GS1.1.1673040348.6.1.1673040997.0.0.0; _dc_gtm_UA-521079-1=1; _gali=lnkMfrPartNumber_1; RT="z=1&dm=mouser.com&si=40dc4710-b3fd-4bb1-8963-db3e2735e649&ss=lcl10xzk&sl=9&tt=h38&bcn=%2F%2F17de4c11.akstat.io%2F&ld=9ly5&nu=1hrtxjd5s&cl=dxfc&ul=dxh8"',
            'pragma':'no-cache',
            'referer': 'https://www.mouser.com',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
    }

    start_urls = [
        
    ]

    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.mouser.com/c/?q=%s' % partnumber]
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
        time.sleep(3)
        current_url = self.driver.current_url ## current_url is the url of the page after the driver.get() command is executed with response.url. If the current_url is different than the start_url, it means that a redirection happened.
        if current_url != self.start_urls[0]:
            sku = self.part_number
            Inventory = self.driver.find_element(By.XPATH, "//*[contains(@class,'onOrderQuantity')]").text
            orderAmount = self.driver.find_elements(By.XPATH, "//*[contains(@class,'text-right pricebreak-col')]")
            prices = self.driver.find_elements(By.XPATH, "//*[contains(@headers,'unitpricecolhdr')]")
            data =[]
            for i in orderAmount:
                data.append({'Distributor':'mouser','SKU':sku, 'Inventory': Inventory, 'quantity': i.text, 'price': prices[orderAmount.index(i)].text, 'ClickUrl': response.url, 'currency': 'USD'})
        else:
            Match = self.driver.find_element(By.XPATH, "//*[contains(@data-mfrpartnumber,'"+self.part_number+"')]")
            if Match:
                data =[]
                sku = self.part_number
                Inventory = Match.find_element(By.XPATH, "td[7]/div/span").text
                orderAmount = Match.find_elements(By.XPATH, "td[8]/table/tbody/tr/th[contains(@class,'PriceBreakQuantity')]")
                prices = Match.find_elements(By.XPATH, "td[8]/table/tbody/tr/td[contains(@class,'PriceBreakPrice')]")

                for i in orderAmount:
                    data.append({'Distributor':'mouser','SKU':sku, 'Inventory': Inventory, 'quantity': i.text, 'price': prices[orderAmount.index(i)].text, 'ClickUrl': response.url, 'currency': 'USD'})

        print(data)
  
     