# PUT RDS connections here
import os

DB_URI = "postgresql://cajitos.c9dujl3wwcyr.us-east-2.rds.amazonaws.com"
DB_PORT = 5432
DB_HOST = 'cajitos.c9dujl3wwcyr.us-east-2.rds.amazonaws.com'
DB_USER = os.environ.get('db_user')
DB_NAME = 'cajitos_db'
DB_PASS = os.environ.get('db_pass')
