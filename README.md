# Project1Group1-S1-2022

# Device Management System

This is a [Flask](https://flask.palletsprojects.com/en/2.0.x/) Web app developed for a software and games company to track their devices.

## Prerequisites

- Python3
- Pip3
- VSCode or PyCharm
- Git

## Development

1. Clone the repository to your local

```
git clone git@github.com:LUMasterOfAppliedComputing/Project1Group1-S1-2022.git
```

2. Create virtual environment

```
# Linux
sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate

# macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -3 -m venv .venv
.venv\scripts\activate

```

3. Install dependencies

```
python3 -m pip install -r requirements.txt
```

4. Copy `config` to `config.py` in the root directory of project

> **Note:** `config.py` has been added into .gitignore, you should always keep the `config.py` file on your local and never check into repository

You can run following command if you are on Linux or macOS, on Windows, `Ctrl + c` and `Ctrl + v` probably is an easy way to copy the file.

```
# Linux
cp config config.py

# macOS
cp config config.py

```

Update configurations to the real values you have on your local, `db_user`, `db_password`, `db_host`, `db_port` and `db_name`

5. Run following command to run your app on your local

```
python3 -m flask run
```

Access http://localhost:5000 to test the app