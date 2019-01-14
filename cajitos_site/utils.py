import os
import random
import secrets
import string
from PIL import Image
from flask import request, abort, current_app
from flask_login import current_user
from flask_mail import Message
from urllib.parse import urlparse, urljoin

from cajitos_site import mail
from cajitos_site.models import VocabularyCard, Post

CONFIRM_ACCOUNT_MESSAGE = """You are registering on Cajitos website
To confirm your email address please visit the following link:"""
RESET_PASSWORD_MESSAGE = """You requested password reset for you account on Cajitos website
To reset your password, visit the following link:"""


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
    return None


def get_cards(search=None):
    search = f"%{search}%" if search else None
    query = VocabularyCard.select()
    if search:
        query = query.where(VocabularyCard.origin_word ** search)
    return query.order_by(VocabularyCard.id.desc()).limit(20)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/user_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def get_post_by_id_and_author(post_id):
    post = Post.get_or_none(Post.id == post_id)
    if not post:
        abort(404)
    if post.author.id != current_user.id:
        current_app.logger.warning('author is not current user, author %s, current user %s', post.author.username,
                                   current_user.username)
        abort(403)
    return post


def send_service_email(user, url_link, confirm_account=True):
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    if confirm_account:
        message_body = CONFIRM_ACCOUNT_MESSAGE
    else:
        message_body = RESET_PASSWORD_MESSAGE
    msg.body = f'''Dear {user.username},
    {message_body}
    {url_link}
    If you did not make this request then simply ignore this email.
'''
    mail.send(msg)


def generate_random_pass(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
