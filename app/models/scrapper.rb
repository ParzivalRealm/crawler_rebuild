class Scrapper < ApplicationRecord
  has_and_belongs_to_many :part_numbers
  has_and_belongs_to_many :suppliers
  has_many :scrapper_attachments
  has_many :attachments, through: :scrapper_attachments
  has_many :scraped_data


 def scrape_and_save(url)
  # Perform web scraping, parsing, and saving of data here
  # For example, you can use the Nokogiri gem to parse the HTML of the webpage, and then use ActiveRecord methods to save the data to the database
  
  scraped_data = Myspider.new()
end

 def generate_attachment
    @attachment = Attachment.new
    @attachment.save
  end
 
 def start_scrape_from_attachment
    @attachment = Attachment.new #esto se va a enviar desde la vista, con el usuario activo y eso.
    @attachment.save_and_scrape
    
 end

  def parsed_for_table
   table_data = {}

    self.scraped_data.each do |data|
      if data.data_type == "price"
        table_data["price"] ||= []
        table_data["price"] << data.data_value
        table_data["supplier_name"] ||= []
        table_data["supplier_name"] << Supplier.find(data.supplier_id).name
        table_data["part_number"] ||= []
        table_data["part_number"] << data.part_number
      end
      if data.data_type == "inventory"
        table_data["inventory"] ||= []
        table_data["inventory"] << data.data_value
      end
    end
   
  
    table_data
  end
end
