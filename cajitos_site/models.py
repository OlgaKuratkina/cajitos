import peewee as pw
import datetime as dt
from cajitos_site import db, login_manager, application
from flask_login import UserMixin


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


@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == int(user_id)).first()


class User(TimestampModel, UserMixin):
    username = pw.CharField(max_length=50)
    status = pw.CharField(max_length=20)
    email = pw.CharField(max_length=50)
    password = pw.CharField(max_length=250)
    first_name = pw.CharField(max_length=50, null=True)
    last_name = pw.CharField(max_length=50, null=True)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    @property
    def is_active(self):
        return True


class Post(TimestampModel):
    title = pw.TextField()
    content = pw.TextField()
    tags = pw.CharField(max_length=50)
    category = pw.CharField(max_length=50)
    author = pw.ForeignKeyField(User, related_name='posts')

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


class ExpressionCard(TimestampModel):
    origin_expression = pw.TextField()
    translation_expression = pw.TextField()
    origin_language = pw.CharField(choices=('es', 'ru', 'en'), default='en')
    author = pw.ForeignKeyField(User, related_name='expressions')
    category = pw.CharField(max_length=50, null=True)


class VocabularyCard(TimestampModel):
    origin_word = pw.TextField()
    translation_word = pw.TextField()
    origin_language = pw.CharField(choices=('es', 'ru', 'en'), default='en')
    part_of_speech = pw.CharField(max_length=50, null=True)
    author = pw.ForeignKeyField(User, related_name='words', null=True)

    def __str__(self):
        return f"'{self.origin_word}' - {self.origin_language} -->  '{self.translation_word}'"


# db.drop_tables([VocabularyCard, User, Post])
db.create_tables([VocabularyCard, User, Post])
