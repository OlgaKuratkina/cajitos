import peewee as pw
import datetime as dt
from cajitos_site import db


class BaseModel(pw.Model):
    class Meta:
        database = db


class TimestampModel(BaseModel):
    created_at = pw.DateTimeField(default=dt.datetime.utcnow)
    modified_at = pw.DateTimeField(default=dt.datetime.utcnow)

    def save(self, **kwargs):
        """Update self modified at."""
        self.modified_at = dt.datetime.utcnow()
        return super(TimestampModel, self).save(**kwargs)


class VocabularyCard(TimestampModel):
    origin_word = pw.TextField()
    translation_word = pw.TextField()
    origin_language = pw.CharField(choices=('es', 'ru', 'en'), default='en')
    part_of_speech = pw.CharField(max_length=50, null=True)

    def __str__(self):
        return f"'{self.origin_word}' - {self.origin_language} -->  '{self.translation_word}'"


class User(TimestampModel):
    username = pw.CharField(max_length=50)
    status = pw.CharField(max_length=20)
    email = pw.CharField(max_length=50)
    password = pw.CharField(max_length=50)
    first_name = pw.CharField(max_length=50, null=True)
    last_name = pw.CharField(max_length=50, null=True)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


class Post(TimestampModel):
    title = pw.TextField()
    content = pw.TextField()
    tags = pw.CharField(max_length=50)
    category = pw.CharField(max_length=50)
    author = pw.ForeignKeyField(User, related_name='posts')

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


db.create_tables([VocabularyCard, User, Post])
