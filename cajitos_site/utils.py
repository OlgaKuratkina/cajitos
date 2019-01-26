import os
import secrets
import string
import peewee as pw
from PIL import Image
from flask import request, current_app
from flask_mail import Message
from urllib.parse import urlparse, urljoin

from cajitos_site import mail

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
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def filter_module(mod, criteria=lambda obj: True):
    """Filter module contents by given criteria."""
    for name in dir(mod):
        item = getattr(mod, name)
        if criteria(item):
            yield item


def get_models_from_module(module):
    return list(filter_module(module, lambda o: isinstance(o, type) and issubclass(o, pw.Model)))
