  class ScrappersController < ApplicationController
    require 'roo' # for reading excel files which are uploaded by the user
    require 'wombat' # for web scraping, but probably i will remove it
    require 'byebug' # for debugging but probably remove it.
    require 'selenium-webdriver' # for web scraping, awesome
    require 'axlsx' # for generating xlsx files with the web scraping results
    require_relative  '../../lib/scrapper_service' # my custom scrapper service class for web scraping

    def index
      @attachments = Attachment.all
    end

    def new
      @scrapper = Scrapper.new
      render 'create_with_attachment'
    end


    def show
      if params[:format] == 'xlsx'
        @scrappers = Scrapper.find(params[:id]).parsed_for_table
        respond_to do |format|
          format.xlsx {
            response.headers['Content-Disposition'] = 'attachment; filename="scrappers.xlsx"'
            render xlsx: 'show'
          }
          format.html { render 'show' }
        end
      else
        @scrappers = Scrapper.find(params[:id]).parsed_for_table
        render 'show'
      end
    end
    #esta es la funcion que va a llamar el formulario de la vista de new, que es la que se va a encargar de crear el scrapper y el attachment.
    def create_with_attachment
      @scrapper = Scrapper.new
      if @scrapper.save
        attachment = Attachment.new(attachable_type: "Scrapper", attachable_id: @scrapper.id)
        attachment.file = params[:scrapper][:attachment]
        if attachment.save
          ScrapperService.new(attachment.file, @scrapper).call
          redirect_to @scrapper
        else
          flash[:error] = "There was an error saving the attachment"
          redirect_to new_scrapper_path
        end
      else
        flash[:error] = "There was an error saving the scrapper"
        redirect_to new_scrapper_path
      end
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

    def save_attachment(attachment_instance)
      attachment_instance.save
    end


    # this method is called when the user clicks on the "Scrape" button on the index page
    # it takes the uploaded file and scrapes the data from the website
    # it then generates an xlsx file with the scraped data and sends it to the user to download.
    #aqui genera toda la web info, pero como este metodo no inicio una instancia de scrapper, la data muere aqui.
  

    # this method is called when the user clicks on the "Generate XLSX" button on the index page, it uses the web_info instance variable values, but they are send as params, i need to make a better solution.
    # i need to save the web_info into the database.
    def generate_xlsx
      @scrappers = Scrapper.find(params[:id]).parsed_for_table
      filename = "scraped_data_#{Time.now.strftime("%Y%m%d%H%M%S")}.xlsx"
      p = Axlsx::Package.new
      wb = p.workbook
      wb.add_worksheet(name: "Scraped Data") do |sheet|
        @scrappers.keys.each do |key|
          sheet.add_row [key.capitalize]
        end
        @scrappers.values.first.count.times do |i|
          row = []
          @scrappers.values.each do |values|
            row << values[i]
          end
          sheet.add_row row
        end
      end
      p.serialize(filename)
      send_file filename, type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename: filename, disposition: 'attachment'
    end
  end



