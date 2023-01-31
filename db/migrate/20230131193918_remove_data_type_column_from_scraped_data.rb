class RemoveDataTypeColumnFromScrapedData < ActiveRecord::Migration[7.0]
  def change
    remove_column :scraped_data, :data_type
  end
end
