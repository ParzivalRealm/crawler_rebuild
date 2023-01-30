class ScrapperService
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
      suppliers_list.each do |supplier|
        base_url = supplier.website
        searchpath = supplier.searchpath.gsub('ssacprtno', row[0])
        url = base_url + searchpath
        self.parse_and_save(self.scrape_info(supplier.name, url, supplier.id, row[0]))
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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0")
    driver = Selenium::WebDriver.for(:firefox, options: options)
    driver.get(url)
    sleep 2
    scrape_info = {}
    self.xpaths(supplier_name).each do |k, v|
      
      scrape_info[k] = driver.find_elements(:xpath, v).map(&:text)
      
      scrape_info["supplier_id"] = supplier_id
      scrape_info["part_number"] = part_number
    end
    driver.quit
    if scrape_info["inventory"].size < scrape_info["price"].size
      scrape_info["inventory"] = scrape_info["inventory"].fill(scrape_info["inventory"].first, scrape_info["inventory"].size, scrape_info["price"].size - scrape_info["inventory"].size)
    end
    scrape_info
  end
  
  def xpaths(supplier_name)
    xpathHash = {}
    case supplier_name
    when "alliedelec"
      xpathHash["price"] = "//*[contains(@class, 'new-material-available-standard-pricing-header-2')]"
      xpathHash["inventory"] = "/html[1]/body[1]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/p[2]"
    when "Mouser"
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    else
      xpathHash["manufacturer"] = "//td[@class='tr-mfg']/a"
    end
    xpathHash
  end
  
  def parse_and_save(scraped_data)
    scraped_data.each do |k, v|
      
      if k == "supplier_id" || k == "part_number"
        next
      else
      v.each do |data|
        #a refactor might be done so it doesnt reference to the part_number but uses the jointables that already exists.
        scraped_data_instance = ScrapedDatum.new(data_type: k, data_value: data, scrapper_id: @scrapper.id, supplier_id: scraped_data["supplier_id"], part_number: scraped_data["part_number"]) 
        scraped_data_instance.save
      end
    end
    end
  end
end
