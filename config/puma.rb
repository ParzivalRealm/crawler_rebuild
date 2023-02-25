#!/usr/bin/env puma

# start puma with:
# RAILS_ENV=production bundle exec puma -C ./config/puma.rb
# or
# RAILS_ENV=development bundle exec puma -C ./config/puma.rb

application_path = Rails.root
railsenv = ENV['RAILS_ENV'] || 'production'
directory application_path
environment railsenv
daemonize true
pidfile "#{application_path}/tmp/pids/puma-#{railsenv}.pid"
state_path "#{application_path}/tmp/pids/puma-#{railsenv}.state"
stdout_redirect
"#{application_path}/log/puma-#{railsenv}.stdout.log"
"#{application_path}/log/puma-#{railsenv}.stderr.log"
threads 0, 16
bind "unix://#{application_path}/tmp/sockets/#{railsenv}.socket"
