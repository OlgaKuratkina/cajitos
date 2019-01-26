from flask import current_app, abort
from flask_login import current_user

from cajitos_site import models as mod


def get_post_by_id_and_author(post_id):
    post = mod.Post.get_or_none(mod.Post.id == post_id)
    if not post:
        abort(404)
    if post.author.id != current_user.id:
        current_app.logger.warning('author is not current user, author %s, current user %s', post.author.username,
                                   current_user.username)
        abort(403)
    return post


def get_cards(search=None):
    search = f"%{search}%" if search else None
    query = mod.VocabularyCard.select()
    if search:
        query = query.where(mod.VocabularyCard.origin_word ** search)
    return query.order_by(mod.VocabularyCard.id.desc()).limit(20)
