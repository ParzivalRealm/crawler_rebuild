class AddPartNumberIdToScrappers < ActiveRecord::Migration[7.0]
  def change
    add_reference :scrappers, :part_number, index: true
  end
end
