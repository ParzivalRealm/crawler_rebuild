# Purpose: To display the home page of the application, which is going to be the login page.
class HomeController < ApplicationController
  before_action :authenticate_user!
  
  def index
    @user = current_user
  end
end