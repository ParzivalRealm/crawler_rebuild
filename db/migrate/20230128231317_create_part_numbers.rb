class CreatePartNumbers < ActiveRecord::Migration[7.0]
  def change
    create_table :part_numbers do |t|
      t.references :supplier, null: false, foreign_key: true
      t.references :scrapper, null: false, foreign_key: true
      t.string :part_number, null: false
      t.string :description, null: false
      t.string :manufacturer, null: false
      t.string :category
      

      t.timestamps
    end
  end
end
