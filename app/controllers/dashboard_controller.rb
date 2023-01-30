class DashboardController < ApplicationController
  before_action :authenticate_user!
  #before_action :authorize_admin, only: [:index]
 

  def index
    case current_user.role
    when 'admin'
      render 'admin_dashboard'
    when 'user'
      render 'user_dashboard'
    else
      redirect_to unauthenticated_root_path
    end
  end
  private

  
  #def authorize_admin
   # unless current_user.role == 'admin'
    #  redirect_to root_path, alert: 'You are not authorized to access this page.'
    #end
  #end

end
