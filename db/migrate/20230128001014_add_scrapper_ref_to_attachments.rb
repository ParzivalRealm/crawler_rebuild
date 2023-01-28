class AddScrapperRefToAttachments < ActiveRecord::Migration[7.0]
  def change
    add_reference :attachments, :scrapper, index: true
  end
end
