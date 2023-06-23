# Spatial Data

## Prerequisites

Create .env on the same directory as the project root and paste these:
```
DATABASE_NAME={your_database_name}
D_USER={your_database_user}
D_PASS={your_user_password}
```

**Local Setup**

Install needed modules for the project can be found in requirements.txt. Compatible with **python 3.x** and above.

Before installing the modules make sure your system has libpq-dev and python-dev

For windows user consider using WSL.

**Ubuntu / Debian**

Installing libpq-dev and python-dev

```
sudo apt-get update
sudo apt-get install libpq-dev python-dev
```

Installing the required modules
```
<your_python> -m pip install -r requirements.txt
```
Make sure your system has **postgresql** and **postgis** extension installed

**Docker**

**Coming Soon**

## Running

Starting the DB server
```
sudo service postgresql start
```

Enter the PostgreSQL interface as the root user
```
sudo -u postgres psql
```




