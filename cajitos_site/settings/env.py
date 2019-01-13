# PUT RDS connections here
import os

PER_PAGE = 3

DB_PORT = 5432
DB_HOST = os.environ.get('db_host')
DB_USER = os.environ.get('db_user')
DB_NAME = os.environ.get('db_name')
DB_PASS = os.environ.get('db_pass')

SECRET_KEY = os.environ.get('SECRET_KEY')

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True

MAIL_USERNAME = os.environ.get('EMAIL_USER')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
