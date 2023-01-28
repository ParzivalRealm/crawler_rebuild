class ScrapperController < ApplicationController
  require 'roo' # for reading excel files which are uploaded by the user
  require 'wombat' # for web scraping, but probably i will remove it
  require 'byebug' # for debugging but probably remove it.
  require 'selenium-webdriver' # for web scraping, awesome
  require 'axlsx' # for generating xlsx files with the web scraping results
  require_relative  '../../lib/my_spider' # my custom spider class for web scraping

  def index
    @attachments = Attachment.all
  end

  def new
    @scrappers = Scrapper.new
  end

  # this sends the appropriate xpaths according the website to be scrapped to an instance of the MySpider class.
  # The MySpider class is in the lib folder and is a custom class for web scraping
  def scrape_price(supplier_name)
    if supplier_name == "alliedelec"
      {
        price: "//*[contains(@class, 'new-material-available-standard-pricing-header-2')]",
        order_amounts: "//*[contains(@class, 'new-material-available-standard-pricing-header-1')]",
        inventory: "/html[1]/body[1]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/p[2]",
      }
    elsif supplier_name == "RS Components"
      "span.price"
    end
  end

  # this method is called when the user clicks on the "Scrape" button on the index page
  # it takes the uploaded file and scrapes the data from the website
  # it then generates an xlsx file with the scraped data and sends it to the user to download.
  #aqui genera toda la web info, pero como este metodo no inicio una instancia de scrapper, la data muere aqui.
  def get_attachment_info(file_id)
     binding.pry
    @attachment_file = Attachment.find(file_id) # get the uploaded file that contains the part numbers the user wants to search, it gets it from the database.
    suppliers_list = Supplier.all # get all the suppliers from the database, this is used to loop through all the suppliers and scrape the data from their websites. The xpaths are generated on another function that handles the logic of web scraping selectors.
    xlsx = Roo::Spreadsheet.open(@attachment_file.file) # open the uploaded file with the part numbers to be searched
    parsed_data = {} # this is the hash that will contain the scraped data that will be used to generate the xlsx file and view it on the browser.

    suppliers_list.each do |supplier| # loop through all the suppliers, set the key for the hash to the supplier name and set the value to an empty array. generates the xpath of the supplier and each row of the xlsx that contains the part number to be searches, then for each row it creates an instance of the MySpider class and calls the web_info method to get the scraped data. which is then set on instance variables to be used by other methods. probably pending to clean some variables.
      parsed_data[supplier.name] = []
      base_url = supplier.website
      xpathHash = scrape_price(supplier.name)
      xlsx.each do |row|
        if row[0].present?
          searchpath = supplier.searchpath.gsub('ssacprtno', row[0])
          spider = MySpider.new(url_base: base_url, path_base: searchpath, part_number: row[0], xpaths: xpathHash)
          parsed_data[supplier.name] << spider.web_info
        end
      end 
    end
    @web_info = parsed_data        
  end

  # this method is called when the user clicks on the "Generate XLSX" button on the index page, it uses the web_info instance variable values, but they are send as params, i need to make a better solution.
  # i need to save the web_info into the database.
  def generate_xlsx
    web_info = params[:web_info]
    filename = "scraped_data_#{Time.now.strftime("%Y%m%d%H%M%S")}.xlsx"
    p = Axlsx::Package.new
    wb = p.workbook
    wb.add_worksheet(name: "Scraped Data") do |sheet|
      sheet.add_row %w{Distributor SKU Inventory Quantity Price}
      web_info.each do |distributor, data|
        data.each do |info|
          sheet.add_row [distributor, info[:sku], info[:inventory], info[:order_amounts], info[:price]]
        end
      end
    end
    p.serialize(filename)
    send_file filename, type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename: filename, disposition: 'attachment'
  end
end



