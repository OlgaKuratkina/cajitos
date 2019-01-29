import logging
import peewee as pw
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import cajitos_site.settings as settings
from configure import configure_app

logger = logging.getLogger(__name__)


db = pw.PostgresqlDatabase(database=None)
    # settings.DB_NAME,
    # user=settings.DB_USER,
    # host=settings.DB_HOST, port=settings.DB_PORT, password=settings.DB_PASS)

bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
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
    db.init(**application.config['DATABASE'])

    from cajitos_site.users.routes import users
    from cajitos_site.blog_posts.routes import posts
    from cajitos_site.misc.routes import misc
    from cajitos_site.errors.routes import errors
    application.register_blueprint(users)
    application.register_blueprint(posts)
    application.register_blueprint(misc)
    application.register_blueprint(errors)

    # Register models
    from . import models as models
    application.models = models

    logger.debug('App created')

    return application


application = create_app()
