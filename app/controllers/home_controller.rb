class HomeController < ApplicationController
  before_action :authenticate_user!

  def index

    # This is the home page
  end
end