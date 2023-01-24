class CreateAttachments < ActiveRecord::Migration[7.0]
  def change
    create_table :attachments do |t|
      t.string :attachment_id polymorphic: true, index: true
      t.string :attachment_type
      t.string :file
      t.string :file_type
      t.string :file_size
      t.string :file_name
      t.timestamps
    end
  end
end
