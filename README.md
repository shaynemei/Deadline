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

## Set Config for Firebase
1. Go to Firebase console for the project
2. Go to `Settings -> General`  
3. Scroll down to `Firebase SDK snippet`
4. Select `Config` and save the scripts as `firebaseConfig.json` in project root following the format of `firebaseConfig_sample.json`
5. Go to `Settings -> Service accounts`
6. Go to `Firebase Admin SDK` tab
7. Scroll down and select `Generate new private key`
8. Save the file in project root folder as `firebaseAdminConfig.json` following the format of `firebaseAdminConfig_sample.json`

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

## Cronjobs

- Since deployment, one cronjob checks for overdue tasks every hour and penalises the group (-5 units of random resources) the user with the overdue task belongs to.
- Since deployment, one cronjob removes all completed and non-completed tasks (hard reset) every Monday at 00:00, timezone set to system timezone at deployment.