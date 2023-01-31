class AddOrderAmountToScrapedDatum < ActiveRecord::Migration[7.0]
  def change
    add_column :scraped_data, :order_amount, :string
  end
end
