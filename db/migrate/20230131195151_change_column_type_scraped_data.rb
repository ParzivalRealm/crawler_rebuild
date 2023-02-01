class ChangeColumnTypeScrapedData < ActiveRecord::Migration[7.0]
  def change
    change_column :scraped_data, :price, 'decimal USING CAST(price AS decimal)'
    change_column :scraped_data, :inventory, 'integer USING CAST(inventory AS integer)'
  end
end