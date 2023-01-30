class Supplier < ApplicationRecord
  has_and_belongs_to_many :part_numbers
  has_and_belongs_to_many :scrapper_data

  def xpaths
    xpathHash = {}
    xpathHash[:price] = self.price_xpath
    xpathHash[:stock] = self.stock_xpath
    xpathHash[:lead_time] = self.lead_time_xpath
    xpathHash
  end

  def price_xpath
    case self.name
      when "Digikey"
        return "//span[@id='priceblock_ourprice']"
      when "Mouser"
        return "//span[@id='ctl00_ctl00_cph1_cph1_pdp_pricing_lblPrice']"
      else
        return ""
    end
  end

  def stock_xpath
    case self.name
      when "Digikey"
        return "//span[@id='qtySpan']"
      when "Mouser"
        return "//span[@id='ctl00_ctl00_cph1_cph1_pdp_pricing_lblStock']"
      else
        return ""
    end
  end

  def lead_time_xpath
    case self.name
      when "Digikey"
        return "//span[@id='lead-time']"
      when "Mouser"
        return "//span[@id='ctl00_ctl00_cph1_cph1_pdp_pricing_lblLeadTime']"
      else
        return ""
    end
  end

end
