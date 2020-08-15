# Deadline

Deadline is a to-do list webapp in a group setting to boost productivity!

## Virtual Environment
We recommend doing server development in a Python3.7 environment.
Run the following commands in the Deadline root directory.
```
python3 -m venv venv/deadline
```

Activate your Deadline virtual environment:
```
source venv/deadline/bin/activate
```

## Installation
Install requirements
```
pip install -r requirements.txt
```

## Run local development
1. Make sure it is executable
```
chmod +x run_local.sh
```

2. Run locally
```
./run_local.sh
```

## Run tests
1. Make sure it is executable
```
chmod +x run_tests.sh
```

2. Run tests, supply with -v to check which functions are tested in each file
```
./run_tests.sh
```

Go to `./htmlconv/index.html` for an interactive coverage report.