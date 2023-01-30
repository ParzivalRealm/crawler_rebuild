class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  enum role: {user: 0, admin: 1, panelshop: 2}
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable
  has_many :attachments, as: :attachable

  before_create :set_default_role

  def admin?
    self.role == "admin"
  end

  def generate_scrapper
    Scrapper.new(self)
  end


  private
    def set_default_role
      self.role ||= :user
    end 

    
end
