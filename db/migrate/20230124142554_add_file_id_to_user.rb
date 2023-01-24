class AddFileIdToUser < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :attachment_id, :string
  end
end
