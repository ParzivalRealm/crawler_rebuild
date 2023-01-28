class RemoveColumnFromAttachments2 < ActiveRecord::Migration[7.0]
  def change
    remove_column :attachments, :users_id
  end
end
