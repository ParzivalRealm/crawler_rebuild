class ChangeColumnTypeScrapedData < ActiveRecord::Migration[7.0]
  def change
    change_column :scraped_data, :price, :decimal
    change_column :scraped_data, :inventory, :integer
  end
end
