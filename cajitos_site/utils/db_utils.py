import random

import peewee as pw
from flask import current_app, abort
from flask_login import current_user

from cajitos_site import models as mod
from cajitos_site.models import User


def get_post_by_id_and_author(post_id):
    post = mod.Post.get_or_none(mod.Post.id == post_id)
    if not post:
        abort(404)
    if post.author.id != current_user.id:
        current_app.logger.warning('author is not current user, author %s, current user %s', post.author.username,
                                   current_user.username)
        abort(403)
    return post


def get_cards_words(search=None):
    search = f"%{search}%" if search else None
    query = mod.VocabularyCard.select()
    if search:
        query = query.where(mod.VocabularyCard.origin ** search)
    return query.order_by(mod.VocabularyCard.id.desc()).limit(30)


def get_cards_expressions(page=0, search=None):
    search = f"%{search}%" if search else None
    query = mod.ExpressionCard.select()
    if search:
        query = query.where(mod.ExpressionCard.origin_expression ** search)
    if page:
        query = query.order_by(mod.ExpressionCard.id.desc()).paginate(
            page=page, paginate_by=current_app.config['PER_PAGE']
        )
    return query


# TODO refactor out common query elements
def get_drink_ingredients(page=0, search=None):
    search = f"%{search}%" if search else None
    query = mod.Ingredient.select()
    if search:
        query = query.where(mod.Ingredient.name ** search)
    if page:
        query = query.order_by(mod.Ingredient.id.desc()).paginate(
            page=page, paginate_by=current_app.config['PER_PAGE']
        )
    return query


def search_model_records(model: pw.Model, page=0, search=None):
    search = f"%{search}%" if search else None
    query = model.select()
    if search:
        query = query.where(model.name ** search)
    if page:
        query = query.order_by(model.id.desc()).paginate(
            page=page, paginate_by=current_app.config['PER_PAGE']
        )
    return query


def cache_data(model, data):
    if not data:
        return None
    if model.get_or_none(model.ext_id == data['ext_id']):
        return model.update(**data)
    else:
        return model.create(**data)


def get_random_record(model):
    records = model.select().order_by(pw.fn.Random()).limit(30)
    return random.choice(records)


def get_user_google(google_id):
    return User.select().where(User.google_id == google_id).first()
