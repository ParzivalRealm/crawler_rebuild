class RemoveSupplierIdAndScrapperIdColumnsToPartNumbers < ActiveRecord::Migration[7.0]
  def change
    remove_column :part_numbers, :supplier_id
    remove_column :part_numbers, :scrapper_id
  end
end
