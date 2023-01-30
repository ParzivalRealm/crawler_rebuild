class CreateJoinTablePartNumbersSuppliers < ActiveRecord::Migration[7.0]
  def change
    create_join_table :part_numbers, :suppliers do |t|
      t.index :part_number_id
      t.index :supplier_id
    end
  end
end
