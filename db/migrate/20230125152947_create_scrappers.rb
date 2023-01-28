class CreateScrappers < ActiveRecord::Migration[7.0]
  def change
    create_table :scrappers do |t|
      t.string :partnumber
      t.integer :order_quantity
      t.integer :price
      t.string :description
      t.string :manufacturer
      t.string :supplier
      t.string :supplier_link
      t.string :amount_required
      t.string :amount_available
      t.string :minimum_order_quantity
      t.string :lead_time
      t.timestamps
    end
  end
end
