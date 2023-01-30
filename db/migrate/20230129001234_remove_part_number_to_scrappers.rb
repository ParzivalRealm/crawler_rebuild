class RemovePartNumberToScrappers < ActiveRecord::Migration[7.0]
  def change
    remove_reference :scrappers, :part_number, index: true
  end
end
