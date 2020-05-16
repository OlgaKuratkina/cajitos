from cajitos_site.settings import env

PER_PAGE = 5

DB_PORT = 5432
DB_HOST = env('DB_HOST', 'localhost')
DB_USER = env('DB_USER', 'postgres')
DB_NAME = env('DB_NAME', 'postgres')
DB_PASS = env('DB_PASS', 'password')

MAIL_USERNAME = 'cajitos.site@gmail.com'

SECRET_KEY = 'test'

DATABASE = {'database': DB_NAME,
            'user': DB_USER,
            'host': DB_HOST,
            'port': DB_PORT,
            'password': DB_PASS}

COCKTAIL_API_URL = 'https://www.thecocktaildb.com/api/json'
COCKTAIL_API_KEY = env('COCKTAIL_API_KEY', '1')
