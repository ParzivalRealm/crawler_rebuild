class RebuildScrapedData < ActiveRecord::Migration[7.0]
  def change
    remove_column :scraped_data, :order_amounts
    remove_column :scraped_data, :price
    
    add_column :scraped_data, :data_type, :string
    add_column :scraped_data, :data_value, :string

  end
end
