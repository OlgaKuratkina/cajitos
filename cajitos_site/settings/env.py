import logging
import os


PER_PAGE = 5


def env(var_name, default=None):
    return os.environ.get(var_name, default)


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

DB_PORT = 5432
DB_HOST = env('DB_HOST')
DB_USER = env('DB_USER')
DB_NAME = env('DB_NAME')
DB_PASS = env('DB_PASS')

# SQLALCHEMY_DATABASE_URI = env('DB_URI', 'sqlite:///:memory:')
# DB_URI = env('DB_URI', "postgresql://postgres@localhost:5433/cajitos")

DATABASE = {'database': DB_NAME,
            'user': DB_USER,
            'host': DB_HOST,
            'port': DB_PORT,
            'password': DB_PASS}

SECRET_KEY = env('SECRET_KEY')

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True

MAIL_USERNAME = env('EMAIL_USER')
MAIL_PASSWORD = env('EMAIL_PASS')
MAIL_DEFAULT_SENDER = env('MAIL_DEFAULT_SENDER')
MAIL_MAX_EMAILS = env('MAIL_MAX_EMAILS', 10)

OWNERS = ['cajitos.site@gmail.com']

COCKTAIL_API_URL = 'https://www.thecocktaildb.com/api/json'
COCKTAIL_API_KEY = env('COCKTAIL_API_KEY', '1')

GOOGLE_CLIENT_ID = env('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = env('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'


logging.warning('Env settings are loaded.')
