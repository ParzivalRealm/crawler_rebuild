class Attachment < ApplicationRecord
  mount_uploader :file, FileUploader
  belongs_to :attachable, polymorphic: true
  belongs_to :scrapper, optional: true

  def create_scrapper_and_attachment
    scrapper = Scrapper.new(attachment: self)
    scrapper.scrap_data
    scrapper.save
  end
end
