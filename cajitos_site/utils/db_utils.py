import random

import markdown
import peewee as pw
from flask import current_app, abort
from flask_login import current_user

from cajitos_site import models as mod
from cajitos_site.models import Post
from cajitos_site.utils.translate_utils import get_language


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
        query = query.where(mod.VocabularyCard.origin ** search | mod.VocabularyCard.translation ** search)
    return query.order_by(mod.VocabularyCard.id.desc())


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
def get_drink_ingredients(search=None):
    search = f"%{search}%" if search else None
    query = mod.Ingredient.select().order_by(mod.Ingredient.name)
    if search:
        query = query.where(mod.Ingredient.name ** search)
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


def create_or_update_post(form, post=None):
    separator = current_app.config['POST_SEPARATOR']
    language = get_language(form.content.data)
    raw_content = form.content.data
    if separator in raw_content:
        preview = raw_content.split(separator, 1)[0]
        preview = markdown.markdown(preview)
    else:
        preview = None
    content = markdown.markdown(form.content.data)
    if post:
        post.title = form.title.data
        post.preview = preview
        post.content = content
        post.category = form.category.data
        post.is_hidden = form.is_hidden.data
        post.language = language
        post.save()
    else:
        Post.create(title=form.title.data, content=content, preview=preview, author=current_user.id, tags='test',
                    category=form.category.data, is_hidden=form.is_hidden.data, language=language)
