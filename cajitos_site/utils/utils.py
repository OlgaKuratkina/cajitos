import importlib
import logging
import os
import pkgutil
import secrets
import string
import peewee as pw
from PIL import Image
from flask import request, current_app, Blueprint, render_template
from flask_mail import Message
from urllib.parse import urlparse, urljoin

from cajitos_site import mail

logger = logging.getLogger(__name__)

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


def generate_random_pass(length=8):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def import_submodules(package_name, *submodules):
    """Import all submodules by package name."""
    results = []
    try:
        package = importlib.import_module(package_name)
    except ImportError as exc:
        logger.warn('Invalid package: %s (%s)', package_name, exc)
        return results

    path = getattr(package, '__path__', None)
    if not path:
        return results

    for _, name, _ in pkgutil.walk_packages(package.__path__):
        if submodules and name not in submodules:
            continue
        try:
            mod_name = "%s.%s" % (package_name, name)
            results.append(importlib.import_module(mod_name))
        except ImportError as exc:
            logger.warn('Invalid module: %s (%s)', mod_name, exc)
            continue

    return results


def filter_module(mod, criteria=lambda obj: True):
    """Filter module contents by given criteria."""
    for name in dir(mod):
        item = getattr(mod, name)
        if criteria(item):
            yield item


def get_models_from_module(module):
    return list(filter_module(
        module, lambda o: isinstance(o, type) and issubclass(o, pw.Model) and 'Model' not in o.__name__)
    )


def register_blueprints(app):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.
    """
    for app_module in app.config['APPS']:
        for mod in import_submodules(app_module):
            for bp in filter_module(mod, lambda item: isinstance(item, Blueprint)):
                print(bp)
                app.register_blueprint(bp)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_bulk_emails(users, subject, text_body, html_body):
    with mail.connect() as conn:
        for user in users:
            msg = Message(recipients=[user.email],
                          body=text_body or html_body,
                          subject=subject)

            conn.send(msg)


def send_service_email(user, url_link, confirm_account=True):
    sender = current_app.config['MAIL_USERNAME']
    recipients = [user.email]
    if confirm_account:
        message_body = CONFIRM_ACCOUNT_MESSAGE
        subject = 'Confirm your account in Cajitos'
    else:
        message_body = RESET_PASSWORD_MESSAGE
        subject = 'Password Reset Request'
    html_body = render_template('email.service_email.html', user=user, url_link=url_link, message_body=message_body)
    txt_body = render_template('email.service_email.txt', user=user, url_link=url_link, message_body=message_body)
    send_email(subject, sender, recipients, text_body=txt_body, html_body=html_body)