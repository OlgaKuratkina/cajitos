import logging
import peewee as pw
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from configure import configure_app

from flask_bootstrap import Bootstrap

logger = logging.getLogger(__name__)


db = pw.Proxy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(application=None, default_settings='cajitos_site.settings'):
    application = Flask(__name__, instance_relative_config=True)

    application.config.from_object(default_settings)
    print(application.config)

    with application.app_context():

        configure_app(application)

    bcrypt.init_app(application)
    login_manager.init_app(application)
    mail.init_app(application)
    moment.init_app(application)
    bootstrap = Bootstrap(application)

    if application.config['TESTING']:
        db.initialize(pw.SqliteDatabase(**application.config['DATABASE']))
    else:
        db.initialize(pw.PostgresqlDatabase(**application.config['DATABASE']))

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
