class AddPathColumnToSuppliers < ActiveRecord::Migration[7.0]
  def change
    add_column :suppliers, :searchpath, :string
  end
end
