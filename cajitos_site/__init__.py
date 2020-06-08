import logging
from datetime import datetime

import peewee as pw
from flask import Flask, request, g
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_moment import Moment

from configure import configure_app

db = pw.Proxy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
babel = Babel()
moment = Moment()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(application=None, default_settings='cajitos_site.settings'):
    application = Flask(__name__, instance_relative_config=True)

    application.config.from_object(default_settings)

    with application.app_context():

        configure_app(application)

    bcrypt.init_app(application)
    login_manager.init_app(application)
    mail.init_app(application)
    moment.init_app(application)
    bootstrap = Bootstrap(application)
    babel.init_app(application)

    if application.config['TESTING']:
        db.initialize(pw.SqliteDatabase(**application.config['DATABASE']))
    else:
        db.initialize(pw.PostgresqlDatabase(**application.config['DATABASE']))
    #  TODO optimize registering blueprints
    from cajitos_site.users.routes import users
    from cajitos_site.bar.routes import bar
    from cajitos_site.blog.routes import blog
    from cajitos_site.misc.routes import misc
    from cajitos_site.errors.routes import errors
    from cajitos_site.service.routes import service
    application.register_blueprint(users)
    application.register_blueprint(blog)
    application.register_blueprint(misc)
    application.register_blueprint(errors)
    application.register_blueprint(service)
    application.register_blueprint(bar)

    # Register models
    from . import models as models
    application.models = models

    application.logger.info('App created')

    return application


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(application.config['LANGUAGES'])


application = create_app()


@application.before_request
def _before():
    if db.is_closed():
        db.connect()
    g.locale = str(get_locale())
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.save()


@application.teardown_request
def _after(exc):
    if not db.is_closed():
        db.close()
