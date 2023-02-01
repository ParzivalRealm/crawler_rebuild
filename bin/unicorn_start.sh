#!/bin/bash
set -e

# Start unicorn
exec bundle exec unicorn -c config/unicorn.rb -E production -D
