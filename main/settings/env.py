# PUT RDS connections here
import os

DB_PORT = 5432
DB_HOST = os.environ.get('db_host')
DB_USER = os.environ.get('db_user')
DB_NAME = os.environ.get('db_name')
DB_PASS = os.environ.get('db_pass')
