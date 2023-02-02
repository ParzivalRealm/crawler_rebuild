class ScrapperService
  require 'net/http'
  require 'uri'
  require 'zlib'
  require 'nokogiri'
  def initialize(attachment_file, scrapper)
    
    @data = {}
    @file = attachment_file
    @xlsx = Roo::Spreadsheet.open(@file)
    @scrapper = scrapper
  end
  
  def call
    #se llama desde el controlador y aqui consigue el file y procesa la info  y la guarda en la base de datos, luego tengo que anadir logica para que en la vista solamente cargue los part numbers que puso en el archivo
    
    suppliers_list = Supplier.all
    parsed_data = []
    
    @xlsx.each  do |row|
      # self.scrape_info("plcity", "https://www.plc-city.com/shop/en/content/search?q=#{row[0]}", 5, row[0]) this is just for testing, delete when done
      suppliers_list.each do |supplier| # here sends the supplier to iterate
        
        base_url = supplier.website
        searchpath = supplier.searchpath.gsub('ssacprtno', row[0])
        url = base_url + searchpath
        if supplier.name == "digikey"
          url = base_url
        end
        self.scrape_info(supplier.name, url, supplier.id, row[0])
      end
    end
  end
  
  def scrape_info(supplier_name, url, supplier_id, part_number)
    #The structure needs to change on the database, so i can add scraped_data_type as a column, and just save like: data_type = "price", manufacturer, etc... So it is easier to query and show, also to handle scrapping errors, as i will threat each scrape data as its own type.
    options = Selenium::WebDriver::Firefox::Options.new
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0(Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0")
    opdionts.add_argument{"--webdriver-executable-path=../geckodriver"}
    driver = Selenium::WebDriver.for(:firefox, options: options)
    driver.get(url)
    sleep 2
    scrape_info = {}
    
    
    
    #supplier_namedebug = "digikey" # delete this line when done debugging and change the line below to supplier_name
    
    case supplier_name # delete this line when done debugging and change the line below to supplier_name
      
    when "alliedelec"
      xpaths = self.xpaths(supplier_name)
      scrape_info["price"] = driver.find_elements(:xpath, xpaths["price"]).map(&:text) rescue ["0"]
      scrape_info["price"] == [] ? scrape_info["price"] = "0": scrape_info["price"] #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
      scrape_info["order_amount"] = driver.find_elements(:xpath, xpaths["order_amount"]).map(&:text) rescue ["0"]
      scrape_info["order_amount"] == [] ? scrape_info["order_amount"] = "0": scrape_info["order_amount"] #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
      
      scrape_info["inventory"] = driver.find_elements(:xpath, xpaths["inventory"]).map(&:text) rescue ["0"]
      scrape_info["inventory"] == [] ? scrape_info["inventory"] = "0": scrape_info["inventory"] #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
      scrape_info["supplier_id"] = supplier_id
      scrape_info["part_number"] = part_number
      scrape_info["price"].each_with_index do |price, idx|
        
        price.gsub!(/[^0-9.]/, '')
        scrape_info["order_amount"][idx].gsub!(/[^0-9]/, '')
      
        scraped_data_instance = ScrapedDatum.new(scrapper_id: @scrapper.id, supplier_id: supplier_id, part_number: part_number, order_amount: scrape_info["order_amount"][idx], inventory: scrape_info["inventory"][idx], price: price)
        scraped_data_instance.save
      end
    
      
    when "plcity"
      item = driver.find_element(:css, "#sniperfast_search .sniperfast_product a") rescue driver.current_url #this means that the product was not found
      links = [item.attribute('href')] rescue [item]
      xpaths = self.xpaths(supplier_name)
      
      links.each do |link|
        driver.get(link)
        sleep 1
        data_value = driver.find_element(:css, ".product_price").text rescue ["0"]
        data_value == [] ? data_value = ["0"] : data_value #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
        scrape_info["price"] = driver.find_element(:xpath, xpaths["price"]).text rescue "0"
        scrape_info["price"] == [] ? scrape_info["price"] = "0": scrape_info["price"] #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
        scrape_info["price"].gsub!(/[^0-9.]/, '')
        scrape_info["inventory"] = driver.find_element(:xpath, xpaths["inventory"]).map(&:text) rescue ["0"]
        scrape_info["inventory"] == [] ? scrape_info["inventory"] = "0": scrape_info["inventory"] #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
        scrape_info["order_amount"] = 1
        scrape_info["supplier_id"] = supplier_id
        scrape_info["part_number"] = part_number
        scraped_data_instance = ScrapedDatum.new(scrapper_id: @scrapper.id, supplier_id: supplier_id, part_number: part_number, order_amount: scrape_info["order_amount"], inventory: scrape_info["inventory"], price: scrape_info["price"]) 
        scraped_data_instance.save
      end
      
      
    when "wiautomation"
      xpaths = self.xpaths(supplier_name)
      item = driver.find_elements(:xpath, "//a[contains(@class, 'product_name')]") rescue driver.current_url #this means that the product was not found
      exact_match = item.select do |i|
        i.attribute('href').downcase.include?(part_number.downcase)
      end
      link = exact_match[0].attribute('href') rescue nil
      
      if link == nil #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next xpath
        
        scrape_info["price"] = 0
        scrape_info["inventory"] = 0
        scrape_info["order_amount"] = 0
        scrape_info["supplier_id"] = supplier_id
        scrape_info["part_number"] = part_number
        scraped_data_instance = ScrapedDatum.new(scrapper_id: @scrapper.id, supplier_id: supplier_id, part_number: part_number, order_amount: scrape_info["order_amount"], inventory: scrape_info["inventory"], price: scrape_info["price"]) 
        scraped_data_instance.save
        return true#this is to stop the method and go to the next supplier
        
      end   
      
      driver.get(link)
      
      sleep 1
      selenium_elements_price = driver.find_elements(:xpath, xpaths["price"])
      selenium_elements_inventory = driver.find_elements(:xpath, xpaths["inventory"])
      
      selenium_elements_price.each_with_index do |selenium_element, idx|
        data_value = selenium_element.text rescue ["0"]
        data_value == [] ? data_value = "0" : data_value #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
        scrape_info["price"] = data_value
        scrape_info["inventory"] = selenium_elements_inventory[idx].text rescue 0
        scrape_info["inventory"] == [] ? scrape_info["inventory"] = "0": scrape_info["inventory"] #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next supplier
        scrape_info["order_amount"] = 1
        scrape_info["supplier_id"] = supplier_id
        scrape_info["part_number"] = part_number
        scraped_data_instance = ScrapedDatum.new(scrapper_id: @scrapper.id, supplier_id: supplier_id, part_number: part_number, order_amount: scrape_info["order_amount"], inventory: scrape_info["inventory"], price: scrape_info["price"])
        scraped_data_instance.save
      end
    # when "digikey"
    #   #this doesnt use selenium, it uses http requests to digikey javascript function, and then parses the response this might get patched by digikey
    #   suggestions = fetch_suggestions(part_number)
    #   suggested_product_numbers = suggestions['suggestedProductNumbers']
    #   link = nil
    #   if suggested_product_numbers.any?
    #     link = 'https://www.digikey.com' + suggested_product_numbers[0]['navigationUrl']
    #   end
      
    #   if link == nil #this means that the product was not found or that the part number is not exact so we just fill the data with "0"and go to next xpath
    #     scrape_info["price"] = 0
        
    #     scrape_info["supplier_id"] = supplier_id
    #     scrape_info["part_number"] = part_number
    #     scrape_info["order_amount"] = "0"
    #     scrape_info["inventory"] = 1
    #     scraped_data_instance = ScrapedDatum.new(scrapper_id: @scrapper.id, supplier_id: supplier_id, part_number: part_number, order_amount: scrape_info["order_amount"], inventory: scrape_info["inventory"], price: scrape_info["price"]) 
    #     scraped_data_instance.save
    #     return true
    #   end
      
    #   page_info = fetch_page(link)
    #   doc = Nokogiri::HTML(page_info)
    #   prices_table = doc.xpath("//table[contains(@class, 'MuiTable-root') and starts-with(@data-testid, 'pricing-table-')]/tbody[contains(@class, 'MuiTableBody-root')]/tr")
    #   prices_table.each do |element|
    #     scrape_info["price"] = element.children[1].text.gsub(/[^0-9.]/, '') rescue ["0"]
    #     scrape_info["order_amount"] = element.children[0].text.gsub(/[^0-9.]/, '') rescue ["0"]
    #     scrape_info["inventory"] = 1 #this is a bit tricky, digikey has a lot of different inventory statuses, so we need to check all of them by doing more js requests, in the meantime everything will be 1
    #     scraped_data_instance = ScrapedDatum.new(scrapper_id: @scrapper.id, supplier_id: supplier_id, part_number: part_number, order_amount: scrape_info["order_amount"], inventory: scrape_info["inventory"], price: scrape_info["price"]) 
    #     scraped_data_instance.save
        
    #   end
      
    when "mouser"
      
    when "mrosupply"
      
    when "onlinecomponents"
      
    when "sager"
      
    when "tti"
      
    when "williamsautomations"
    else
      #remove this when all suppliers are added
    end
    
    driver.quit
  end
  
  
  def xpaths(supplier_name)
    xpathHash = {}
    case supplier_name
    when "alliedelec"
      xpathHash["price"] = "//*[contains(@class, 'new-material-available-standard-pricing-header-2')]"
      xpathHash["order_amount"] = "//*[contains(@class, 'new-material-available-standard-pricing-header-1')]"
      xpathHash["inventory"] = "/html[1]/body[1]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/p[2]"
    when "plcity"
      xpathHash["price"] = "//div[contains(@class,'our_price_display')]"
      xpathHash["inventory"] = "//div[contains(@class,'avilability_status')]"
    when "wiautomation"
      xpathHash["price"] = "//div[contains(@class,'wrap_comp_product_buy_info')]//div[contains(@class, 'main_product_price')]//div[contains(@class, 'price')]"
      xpathHash["inventory"] = "//div[contains(@class,'stock_label')]"
    when "digikey"
      xpathHash["price"] = "//table[contains(@class, 'MuiTable-root') and starts-with(@data-testid, 'pricing-table-')]"
      xpathHash["inventory"] = "//div[@data-testid='price-and-procure-title']"
    when "mouser"
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    when "mrosupply"
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    when "onlinecomponents"
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    when "sager"
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    when "tti"
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    when "williamsautomations"
    else
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    end
    xpathHash
  end
  
  
  def fetch_suggestions(query)
    uri = URI("https://www.digikey.com/suggestions/v3/search")
    params = { keywordPrefix: query, maxSuggestions: 5 }
    uri.query = URI.encode_www_form(params)
    
    headers = {
      ':authority' => 'www.digikey.com',
      ':method' => 'GET',
      ':path' => "#{uri.path}?#{uri.query}",
      ':scheme' => 'https',
      'accept' => '*/*',
      'accept-encoding' => 'gzip, deflate, br',
      'accept-language' => 'en,en-US;q=0.9,es;q=0.8',
      'cache-control' => 'no-cache',
      'lang' => 'en',
      'pragma' => 'no-cache',
      'referer' => 'https://www.digikey.com/',
      'sec-ch-ua' => '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile' => '?0',
      'sec-ch-ua-platform' => '"Linux"',
      'sec-fetch-dest' => 'empty',
      'sec-fetch-mode' => 'cors',
      'sec-fetch-site' => 'same-origin',
      'site' => 'US',
      'user-agent' => 'Mozilla/5."0"(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0."0"Safari/537.36',
      'x-currency' => 'USD'
    }
    
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.start
    request = Net::HTTP::Get.new(uri.request_uri, headers)
    sleep 2
    response = http.request(request)
    JSON.parse(response.body)
  end
  
  
  def fetch_page(url)
    uri = URI(url)
    
    headers = {
      'accept' => 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-encoding' => 'gzip, deflate, br',
      'accept-language' => 'en,en-US;q=0.9,es;q=0.8',
      'cache-control' => 'no-cache',
      'pragma' => 'no-cache',
      'sec-ch-ua' => '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile' => '?0',
      'sec-ch-ua-platform' => '"Linux"',
      'sec-fetch-dest' => 'document',
      'sec-fetch-mode' => 'navigate',
      'sec-fetch-site' => 'same-origin',
      'sec-fetch-user' => '?1',
      'upgrade-insecure-requests' => '1',
      'user-agent' => 'Mozilla/5."0"(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0."0"Safari/537.36'
    }
    
    response = Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == 'https') do |http|
      request = Net::HTTP::Get.new(url)
      headers.each do |key, value|
        request[key] = value
      end
      
      http.request(request)
    end
    if response['content-encoding'] == 'gzip'
      body = Zlib::GzipReader.new(StringIO.new(response.body)).read
    else
      body = response.body
    end
    
    body
  end
  
  
  def parse_and_save(scraped_data)
    scraped_data.each do |k, v|
      
      if k == "supplier_id" || k == "part_number"
        next
      else
        v.each do |data|
          #a refactor might be done so it doesnt reference to the part_number but uses the jointables that already exists.
          scraped_data_instance = ScrapedDatum.new(data_type: k, data_value: data, scrapper_id: @scrapper.id, supplier_id: scraped_data["supplier_id"], part_number: scraped_data["part_number"],order_amount: scraped_data["order_amount"], inventory: scraped_data["inventory"]) 
          scraped_data_instance.save
        end
      end
    end
  end
  
end
