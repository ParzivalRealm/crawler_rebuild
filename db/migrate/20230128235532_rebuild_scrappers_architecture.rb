class RebuildScrappersArchitecture < ActiveRecord::Migration[7.0]
  def change
    remove_column :scrappers, :scrapper_type
    remove_column :scrappers, :result
    remove_column :scrappers, :supplier_id
    add_column :scrappers, :price, :integer
    add_column :scrappers, :availablequantity, :integer
    add_column :scrappers, :minimumorderquantity, :integer
    add_column :scrappers, :leadtime, :integer
  end
end
