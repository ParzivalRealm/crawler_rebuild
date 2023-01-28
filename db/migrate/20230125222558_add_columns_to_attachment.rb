class AddColumnsToAttachment < ActiveRecord::Migration[7.0]
  def change
    add_column :attachments, :attachable_type, :string
    add_column :attachments, :attachable_id, :integer
    add_index :attachments, [:attachable_type, :attachable_id]
  end
end
