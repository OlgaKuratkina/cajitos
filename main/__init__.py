import peewee

from main import settings

from settings import DB_PORT, DB_HOST, DB_USER, DB_NAME

db = peewee.PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    host=DB_HOST, port=DB_PORT)
