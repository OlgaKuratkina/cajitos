import peewee as pw

from main.settings import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS

db = pw.PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    host=DB_HOST, port=DB_PORT, password=DB_PASS)


def init_db():
    from main.models import VocabularyCard
    db.create_tables([VocabularyCard])


def clean_db():
    from main.models import VocabularyCard
    VocabularyCard.delete()


if __name__ == "__main__":
    clean_db()
