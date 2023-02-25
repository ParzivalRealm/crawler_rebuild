#!/usr/bin/env puma

# start puma with:
# RAILS_ENV=production bundle exec puma -C ./config/puma.rb
# or
# RAILS_ENV=development bundle exec puma -C ./config/puma.rb

#!/usr/bin/env puma

# Define variables for the application path and environment.
application_path = Rails.root
rails_env = ENV['RAILS_ENV'] || 'production'

# Configure the application path, environment, and daemonization.
directory application_path
environment rails_env
daemonize true

# Set the location of the PID and state files.
pidfile "#{application_path}/tmp/pids/puma-#{rails_env}.pid"
state_path "#{application_path}/tmp/pids/puma-#{rails_env}.state"

# Set the locations for standard output and error logs.
stdout_redirect "#{application_path}/log/puma-#{rails_env}.stdout.log",
  "#{application_path}/log/puma-#{rails_env}.stderr.log", true

# Set the number of threads to use.
threads 0, 16

# Bind to a Unix domain socket and use nginx as a reverse proxy.
bind "unix://#{application_path}/tmp/sockets/#{rails_env}.socket"
bind "tcp://127.0.0.1:8080"

# Allow puma to be restarted by touch command.
restart_command 'touch tmp/restart.txt'