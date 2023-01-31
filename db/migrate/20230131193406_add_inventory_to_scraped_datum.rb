class AddInventoryToScrapedDatum < ActiveRecord::Migration[7.0]
  def change
    add_column :scraped_data, :inventory, :string
  end
end
