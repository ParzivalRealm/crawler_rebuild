class AddPriceToScrapedData < ActiveRecord::Migration[7.0]
  def change
    add_column :scraped_data, :price, :string
  end
end
