class AddFileColumnToAttachments < ActiveRecord::Migration[7.0]
  def change
    add_column :attachments, :file, :string
  end
end
