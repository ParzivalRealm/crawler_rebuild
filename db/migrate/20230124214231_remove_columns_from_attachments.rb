class RemoveColumnsFromAttachments < ActiveRecord::Migration[7.0]
  def change
    remove_column :attachments, :attachment_id
    remove_column :attachments, :attachment_type
    remove_column :attachments, :file
    remove_column :attachments, :file_type
    remove_column :attachments, :file_size
    remove_column :attachments, :file_name
  end
end
