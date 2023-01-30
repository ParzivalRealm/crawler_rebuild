class Attachment < ApplicationRecord
  mount_uploader :file, FileUploader
  belongs_to :attachable, polymorphic: true
  has_many :scrapper_attachments
  has_many :scrappers, through: :scrapper_attachments

  def save_and_scrape
    if self.save
        self.create_scrapper_and_attachment
    end
  end

  def create_scrapper_and_attachment
    @scrapper = Scrapper.new
    @scrapper.attachments << self
    @scrapper.parse_attachment_info(self)
end
end
