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
    name = "masterelectronics"
#cookies to try to bypass:
# :authority: www.masterelectronics.com
# :method: GET
# :path: /en/keywordsearch?text=2904602
# :scheme: https
# accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# accept-encoding: gzip, deflate, br
# accept-language: en,en-US;q=0.9,es;q=0.8
# cache-control: no-cache
# cookie: _gcl_au=1.1.1455291569.1672433086; _ga=GA1.2.137844638.1672433086; _fbp=fb.1.1672433086736.57332189; zaius_js_version=2.21.4; z_idsyncs=; vtsrc=isCampaign%3Dtrue%7Csource%3Doctopart%7Ccampaign%3Doctopart%7Cmedium%3Dinventoryrefferal%7Ckeywords%3D2302227; __zlcmid=1DglUPYdu7Ug1wY; nlbi_837075=rKyoPbzwoCaIWhYpK260ywAAAACZq4oz7oUQZund8lxJ4rug; incap_ses_1061_837075=GmKGPz+qKgH2IY6Pzm65Dmspt2MAAAAANVpyRhPBcIERPW2xyAV+Og==; .Nop.Antiforgery=CfDJ8G7lVdVubfpBuMGv2RioLFGA2ZpXCuUh5naXSIPjBnQbSuiah5X39-7BHOhOoxSbOEZ5aYTEurcbsGuRzOvbdy7XRx62OXbQI9neKNRc-gWipbKqhczo-qZZE9lSr1QdSQ1hmYCbcTJ2wH5N8cjQGJ0; _gid=GA1.2.1038209337.1672948077; ln_or=eyI0NDMyMDQiOiJkIn0%3D; _hc_exp={*_cr*!1672948077520}; visid_incap_837075=TLqO9EbjT9uWLx861twl8bpNr2MAAAAAQ0IPAAAAAACA5HOpAQC6caBu8S8zexWPoowJg2Zx1KZj; CookieConsent={stamp:%27enkTsU5bpzS+rCMdl8Y9h92Eh0k+mdETJ6MJpB1C0FKcfqc/Z7GkJg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1672948102457%2Cregion:%27mx%27}; .Nop.RecentlyViewedProducts=49667233%2C12149964; InternalReferer=kyWrdSrch; mp_5c4c0b7547375eca93e219f6cdf9fbfc_mixpanel=%7B%22distinct_id%22%3A%20%2218564c7b1baca2-0883c4498c25c2-1f462c6d-1fa400-18564c7b1bb1a08%22%2C%22%24device_id%22%3A%20%2218564c7b1baca2-0883c4498c25c2-1f462c6d-1fa400-18564c7b1bb1a08%22%2C%22utm_source%22%3A%20%22octopart%22%2C%22utm_medium%22%3A%20%22inventoryrefferal%22%2C%22utm_campaign%22%3A%20%22octopart%22%2C%22utm_term%22%3A%20%222302227%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Foctopart.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22octopart.com%22%7D; AWSALB=SVRqZJSkDrJdbMNX/RbErxPo1QNQNu5raR/EF8iM6F0Y+6X8T4HiWNbKvbqpAVBfzemm74lr/9mu7tcga+lpVay3i59AghsqolEx2JxCwt3c1QM2lY/MYrjlkmsG; AWSALBCORS=SVRqZJSkDrJdbMNX/RbErxPo1QNQNu5raR/EF8iM6F0Y+6X8T4HiWNbKvbqpAVBfzemm74lr/9mu7tcga+lpVay3i59AghsqolEx2JxCwt3c1QM2lY/MYrjlkmsG; .Nop.Customer=d3524e89-cbab-41b0-8e93-dfbc3b06ef54; .Nop.TempData=CfDJ8G7lVdVubfpBuMGv2RioLFHDpl6B8Ot0w6acZI-2P963C8X3GFqLXe1sfX4g_DgxKNobeaOlf6oUlpIPvUunlr777mmOVbZT3aH7Bp5hYcovO_0qu1NYu6pWvsVVuedy9VBieO3MqqlZU8h_TiIZhPV2X5P5_417e3IfccUPzAQo; vuid=b0ed0842-71bb-4e41-928a-6d2f2d2f6fc7%7C1672948128724; cto_bundle=BrQx619JcEc5OE5vcTV1QmJqcXZmSk5ReHlNR2l4amVZY2w3MzN5VWZTcEZTandwaVc0MjRrTjNoUjJHSzV0TmRXR01USldZVmUlMkZ0JTJCT2ZsRzVQU1hUQUtOcWV1NDF4VDQzRlU4Y1FLd1J3WmNCSXVjZTJwYWh4aW1uQjZtZGFQU0t2WmVRNyUyQm1JVXRFSDVzJTJCdmFnOEtTYmRhaG1vUlFTTXByUHNHdTJiZUJpbm5lbyUzRA; incap_ses_208_837075=HeaRW/xX5VnNE35BpffiAhIyt2MAAAAAl+eqqG6CcLvSWGDaHmHTjQ==; _hc_vid={*id*!*7d897245-d170-4e29-9f32-bc81c6448c2d*~*created*!1672433086656~*psq*!6~*ord*!19~*cl*!6~*gbl*!0}; _hc_ses={*id*!*1380730f-27ae-43f3-9652-2db2ef9576d3*~*created*!1672948077517~*isNew*!false~*psq*!5~*ord*!17~*cl*!6~*ser*!false~*attr*![*(direct)*~*direct*~*(not+set)*~*(not+set)*~*(none)*~*(direct)*]~*ap*!*home*}
# pragma: no-cache
# referer: https://www.masterelectronics.com/en/
# sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Linux"
# sec-fetch-dest: document
# sec-fetch-mode: navigate
# sec-fetch-site: same-origin
# sec-fetch-user: ?1
# upgrade-insecure-requests: 1
# user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36


    start_urls = [
        
    ]
    def __init__(self, partnumber, *args, **kwargs):
        self.start_urls = ['https://www.masterelectronics.com/en/keywordsearch?text=%s' % partnumber]
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
        bypass = self.driver.find_elements(By.XPATH, "//body")
        bypass[0].click()
        time.sleep(5)
        Inventory = self.driver.find_element(By.XPATH, "//*[contains(@id, 'divInInstock')]").text
        sku = self.part_number
        orderAmount = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'col-xs-4 c-part-detail__pricing-quantity')]")
        pricesInfo = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'col-xs-4 c-part-detail__pricing-price')]")
        orderAmount.pop(0)
        pricesInfo.pop(0)
        data = []
        for i in orderAmount:
            quantity = i.text
            price = pricesInfo[orderAmount.index(i)].text
            data.append({'Distributor': 'onlinecomponents', 'SKU': sku, 'Inventory': Inventory, 'quantity': quantity, 'price': price, 'ClickUrl': response.url, 'currency': 'USD'})
  
        print (data)


    