class CreateScrapedData < ActiveRecord::Migration[7.0]
  def change
    create_table :scraped_data do |t|
      t.integer :order_amounts
      t.integer :price
      t.integer :supplier_id
      t.integer :scrapper_id
      t.timestamps
    end
  end
end
