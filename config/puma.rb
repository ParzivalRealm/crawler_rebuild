workers Integer(ENV['WEB_CONCURRENCY'] || 2)
threads_count = Integer(ENV['RAILS_MAX_THREADS'] || 5)
threads threads_count, threads_count

preload_app!

rackup DefaultRackup
port ENV['PORT'] || 3000
environment ENV['RACK_ENV'] || 'development'

bind "tcp://146.190.126.182:#{port}"


#Set the number of workers to at least the number of cores
workers ENV.fetch("WEB_CONCURRENCY") { 2 }

#Min and Max threads per worker
threads_count = ENV.fetch("RAILS_MAX_THREADS") { 5 }
threads threads_count, threads_count
#Set up socket location
bind "unix://#{Rails.root}/tmp/sockets/puma.sock"
# Logging
stdout_redirect "#{Rails.root}/log/puma.stdout.log", "#{Rails.root}/log/puma.stderr.log", true
# Set master PID and state locations
pidfile "#{Rails.root}/tmp/pids/puma.pid"
state_path "#{Rails.root}/tmp/pids/puma.state"

activate_control_app