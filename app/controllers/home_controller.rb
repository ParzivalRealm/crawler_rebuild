# Purpose: To display the home page of the application, which is going to be the login page.
class HomeController < ApplicationController
  
  def index
    if user_signed_in?
      redirect_to authenticated_root_path
    else
      redirect_to unauthenticated_root_path
    end
  end
end