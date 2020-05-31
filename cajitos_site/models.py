import peewee as pw
import datetime as dt
from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from playhouse.postgres_ext import *

from cajitos_site import db, login_manager, bcrypt
from flask_login import UserMixin

from cajitos_site.utils.utils import generate_random_pass


class BaseModel(pw.Model):
    class Meta:
        database = db


class TimestampModel(BaseModel):
    created_at = pw.DateTimeField(default=dt.datetime.utcnow)
    modified_at = pw.DateTimeField(default=dt.datetime.utcnow)

    def save(self, **kwargs):
        """Update self modified at.
        Only exception - User class"""
        if not isinstance(self, User):
            self.modified_at = dt.datetime.utcnow()
        return super(TimestampModel, self).save(**kwargs)


@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == int(user_id)).first()


class User(TimestampModel, UserMixin):
    username = pw.CharField(max_length=1000, unique=True)
    google_id = pw.CharField(max_length=1000, unique=True)
    status = pw.CharField(max_length=20, default='New')
    email = pw.CharField(max_length=50, unique=True, index=True)
    password = pw.CharField(max_length=250)
    first_name = pw.CharField(max_length=50, null=True)
    last_name = pw.CharField(max_length=50, null=True)
    profile_picture = pw.CharField(max_length=100, default='anon.jpg')
    about_me = pw.CharField(max_length=250, null=True)
    last_seen = pw.DateTimeField(default=dt.datetime.utcnow)
    is_admin = pw.BooleanField(default=False)
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

    @classmethod
    def get_user_by_email(cls, email):
        return cls.select().where(cls.email == email).first()

    @property
    def picture_url(self):
        if self.google_id:
            return self.profile_picture
        else:
            return url_for('static', filename='images/user_pics/' + self.profile_picture)

    @classmethod
    def create(cls, **query):
        query['password'] = bcrypt.generate_password_hash(generate_random_pass()).decode('utf-8')
        return super().create(**query)

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
        followed = Post.select().join(Followers, on=(
            (Post.author == Followers.followed_user)
            & (Followers.following_user == self)
        ))
        return followed.union(self.posts).order_by(Post.created_at.desc())


class Followers(TimestampModel):
    followed_user = pw.ForeignKeyField(model=User, backref='following')
    following_user = pw.ForeignKeyField(model=User, backref='followed')


class Post(TimestampModel):
    title = pw.CharField(max_length=100)
    content = pw.TextField()
    tags = pw.CharField(max_length=50)
    category = pw.CharField(max_length=50)
    author = pw.ForeignKeyField(User, backref='posts')
    is_hidden = pw.BooleanField(default=False)
    is_confirmed = pw.BooleanField(default=False)
    language = pw.CharField(max_length=10)

    def __repr__(self):
        return f"Post(title={self.title}, author={self.author})"


class Comment(TimestampModel):
    post_id = pw.ForeignKeyField(model=Post, backref='comments')
    content = pw.TextField()
    author = pw.ForeignKeyField(User, backref='posts')

    def __repr__(self):
        return f"Comment(post={self.post_id}, author={self.author})"


class ExpressionCard(TimestampModel):
    origin_expression = pw.TextField()
    translation_expression = pw.TextField()
    origin_language = pw.CharField(choices=('es', 'ru', 'en'), default='en')
    author = pw.ForeignKeyField(User, backref='expressions')
    category = pw.CharField(max_length=50, null=True)


class VocabularyCard(TimestampModel):
    origin = pw.TextField(unique=True)
    translation = pw.TextField()
    language = pw.CharField(choices=('es', 'ru', 'en'), default='en')
    part_of_speech = pw.CharField(
        choices=('noun', 'pronoun', 'verb', 'adjective', 'adverb', 'preposition', 'conjunction', 'interjection'),
        default='noun')
    author = pw.ForeignKeyField(User, backref='words', null=True)

    def __str__(self):
        return f"'{self.origin}' - {self.language} -->  '{self.translation}'"


class Drink(TimestampModel):
    ext_id = pw.IntegerField(unique=True)
    name = pw.TextField()
    is_alcoholic = pw.BooleanField(default=True)
    instruction = pw.TextField()
    ingredients = JSONField()
    category = pw.TextField(null=True)
    image = pw.CharField(max_length=100, null=True)
    glass = pw.CharField(max_length=100, null=True)


class Ingredient(TimestampModel):
    ext_id = pw.IntegerField(unique=True)
    name = pw.TextField()
    alcohol = pw.TextField(null=True)
    is_alcoholic = pw.BooleanField(default=True)
    description = pw.TextField(null=True)
    category = pw.TextField(null=True)
    image = pw.CharField(max_length=100, null=True)
