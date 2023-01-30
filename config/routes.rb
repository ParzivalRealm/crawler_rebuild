Rails.application.routes.draw do

  resources :suppliers
  resources :part_numbers
  resources :attachments, only: [:new, :create]
  resources :dashboards, only: [:index]
  resources :scrappers
  devise_for :users

  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")

  resources :scrappers do
    post :create_with_attachment, on: :collection
    member do
      get 'generate_xlsx'
    end
  end

  devise_scope :user do
    authenticated :user do
      root 'dashboard#index', as: :authenticated_root
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
