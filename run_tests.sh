#!/bin/bash

# Check if in the right working directory.
if [ ! -d "webapp" ]; then
  echo "You are supposed to run this script in the Deadline root directory."
  exit 1
fi

# Check if in Deadline virtual environment.
source venv/deadline/bin/activate || exit 1;

# set python path variable
export PYTHONPATH=${PYTHONPATH}:$PWD:

# run pytest
pytest "$1"

# check coverage
coverage report

# show in html which lines were covered
coverage html