class CreateScrapper < ActiveRecord::Migration[7.0]
  def change
    create_table :scrappers do |t|
      t.string :scrapper_type
      t.text :result
      t.references :supplier, null: false, foreign_key: true

      t.timestamps
    end
  end
end
