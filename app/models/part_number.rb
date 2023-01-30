class partNumber < ApplicationRecord
  has_and_belongs_to_many :suppliers
  has_and_belongs_to_many :scrapper_data
end