class DropTableJoinTablePartNumberScrapperData < ActiveRecord::Migration[7.0]
  def change
    drop_table :part_numbers_scrapper_data
  end
end
