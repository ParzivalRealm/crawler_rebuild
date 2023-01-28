Rails.application.routes.draw do
  resources :suppliers
  resources :attachments, only: [:new, :create]
  get '/crawler', to: 'attachments#new'
  devise_for :users

  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  devise_scope :user do
    authenticated :user do
      root 'attachments#new', as: :authenticated_root
    end
  
    unauthenticated do
      root 'devise/sessions#new', as: :unauthenticated_root
    end
  end

  # Defines the home path route ("/home")
  get 'home/index'

  get '/generate_xlsx' => 'scrapper#generate_xlsx'

  get 'scrapper/get_attachment_info'
end
