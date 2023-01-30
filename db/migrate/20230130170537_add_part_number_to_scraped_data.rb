class AddPartNumberToScrapedData < ActiveRecord::Migration[7.0]
  def change
    add_column :scraped_data, :part_number, :string
  end
end
