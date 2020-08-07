#!/bin/bash

# Check if in the right working directory.
if [ ! -d "webapp" ]; then
  echo "You are supposed to run this script in the Deadline root directory."
  exit 1
fi

# Check if in Deadline virtual environment.
source venv/deadline/bin/activate || exit 1;

# Run webapp locally
export FLASK_APP=webapp
flask run
