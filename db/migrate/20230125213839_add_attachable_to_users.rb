class AddAttachableToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :attachable, :string
  end
end
