class MySpider  
  require 'wombat'
  require 'byebug'
  attr_accessor :url_base, :path_base, :part_number, :inventory, :prices
  include Wombat::Crawler

  def initialize(url_base:, path_base:, part_number:, xpaths:)
    @url_base = url_base
    @path_base = path_base
    @xpaths = xpaths
    @part_number = part_number
    @url = @url_base + @path_base
    @data = {}
  end

  def web_info
    options = Selenium::WebDriver::Firefox::Options.new
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0")
    driver = Selenium::WebDriver.for(:firefox, options: options)
    driver.get(@url)
    sleep 2
    @xpaths.each do |k, v|
        @data[k] = driver.find_elements(:xpath, v).map(&:text)
    end
    driver.quit
    return @data
  end

end

