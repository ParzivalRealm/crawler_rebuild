class CreateJoinTablePartNumbersScrapperData < ActiveRecord::Migration[7.0]
  def change
    create_join_table :part_numbers, :scrapper_data do |t|
      t.index :part_number_id
      t.index :scrapper_data_id
    end
  end
end
