class RegenerateJoinTablePartNumbersScrapedData < ActiveRecord::Migration[7.0]
  def change
    create_join_table :part_numbers, :scraped_data do |t|
      t.index :part_number
      t.index :scraped_data
    end
  end
end
