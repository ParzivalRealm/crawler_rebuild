class AddCorrectColumnsAttachments < ActiveRecord::Migration[7.0]
  def change
    add_column :attachments, :users_id, :string
  end
end
