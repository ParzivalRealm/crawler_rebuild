class Attachment < ApplicationRecord
  mount_uploader :attachment_id, FileUploader
  belongs_to :attachable, polymorphic: true
end
