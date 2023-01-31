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


    new_data_structure = {}
    self.scraped_data.each do |scraped_datum|
      supplier_id = Supplier.find(scraped_datum.supplier_id).name
      supplier_data = new_data_structure[supplier_id] ||= {}
      part_number = scraped_datum.part_number
      part_number_data = supplier_data[part_number] ||= []
      part_number_data << {
        order_amount: scraped_datum.order_amount,
        inventory: scraped_datum.inventory,
        price: scraped_datum.price,
        created_at: scraped_datum.created_at
      }
    end
    new_data_structure
  end
end
