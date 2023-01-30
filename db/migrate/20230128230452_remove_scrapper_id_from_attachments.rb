class RemoveScrapperIdFromAttachments < ActiveRecord::Migration[7.0]
  def change
    remove_column :attachments, :scrapper_id
  end
end
