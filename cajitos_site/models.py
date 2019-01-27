import peewee as pw
import datetime as dt
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from cajitos_site import db, login_manager
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
    return User.select().get(User.id == int(user_id))


class User(TimestampModel, UserMixin):
    username = pw.CharField(max_length=50, unique=True)
    status = pw.CharField(max_length=20, default='New')
    email = pw.CharField(max_length=50, unique=True, index=True)
    password = pw.CharField(max_length=250)
    first_name = pw.CharField(max_length=50, null=True)
    last_name = pw.CharField(max_length=50, null=True)
    profile_picture = pw.CharField(max_length=50, default='anon.jpg')
    about_me = pw.CharField(max_length=250, null=True)
    last_seen = pw.DateTimeField(default=dt.datetime.utcnow)
    # followers = pw.ManyToManyField(model=self, backref='courses')

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def get_validation_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.get_by_id(user_id)

    @property
    def is_authenticated(self):
        if super().is_authenticated and self.status == 'Confirmed':
            return True
        return False

    def is_following(self, user):
        return Followers.select().where(
            Followers.followed_user == user
            & Followers.following_user == self
        ).all() > 0

    def follow(self, user):
        if not self.is_following(user):
            Followers(Followers.followed_user == user, Followers.following_user == self).save()

    def unfollow(self, user):
        if self.is_following(user):
            Followers(Followers.followed_user == user, Followers.following_user == self).delete_instance()

    def followed_posts(self):
        return Post.select().join(Followers, on=(
            (Post.author == Followers.followed_user)
            & (Followers.following_user == self)
        )).order_by(Post.created_at.desc())


class Followers(TimestampModel):
    followed_user = pw.ForeignKeyField(model=User, backref='following')
    following_user = pw.ForeignKeyField(model=User, backref='followed')


class Post(TimestampModel):
    title = pw.CharField(max_length=100)
    content = pw.TextField()
    tags = pw.CharField(max_length=50)
    category = pw.CharField(max_length=50)
    author = pw.ForeignKeyField(User, backref='posts')

    def __repr__(self):
        return f"Post(title={self.title}, author={self.author})"


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
