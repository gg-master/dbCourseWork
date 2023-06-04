Before launching the application, create .env file (or set environment variables) with the following parameters:
```
PYTHONPATH="src"

SECRET_KEY="your secret key here"

ADMIN_LOGIN="admin"
ADMIN_PASSWD="admin"
                
DB_HOST="localhost"
DATABASE_NAME="public_transport_app"
DB_USER="postgres"
DB_USER_PASSWD="user_password"
```

After creating the .env file, change the path to it in run.py.