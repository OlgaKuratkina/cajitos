import csv
import importlib
import logging
import os

import peewee as pw
import pkgutil
import secrets
import string

from PIL import Image
from flask import request, current_app, Blueprint
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)


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

    output_size = (150, 150)
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


def strip_nulls(src):
    return (line.replace('\0', '') for line in src)


def dict_read_csv(src):
    return csv.DictReader(strip_nulls(src))


def read_csv(file_name):
    file_path = os.path.join(current_app.root_path, file_name)
    with open(file_path, mode='r') as infile:
        return list(csv.DictReader(strip_nulls(infile)))
