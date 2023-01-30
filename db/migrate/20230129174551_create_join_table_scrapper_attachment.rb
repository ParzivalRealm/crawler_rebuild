class CreateJoinTableScrapperAttachment < ActiveRecord::Migration[7.0]
  def change
    create_join_table :scrappers, :attachments do |t|
      t.index [:scrapper_id, :attachment_id]
      t.index [:attachment_id, :scrapper_id]
    end
  end
end
