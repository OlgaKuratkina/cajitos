import peewee as pw
from flask import Flask, request
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from configure import configure_app

from flask_bootstrap import Bootstrap

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
    from cajitos_site.blog_posts.routes import posts
    from cajitos_site.misc.routes import misc
    from cajitos_site.errors.routes import errors
    from cajitos_site.service.routes import service
    application.register_blueprint(users)
    application.register_blueprint(posts)
    application.register_blueprint(misc)
    application.register_blueprint(errors)
    application.register_blueprint(service)

    # Register models
    from . import models as models
    application.models = models

    application.logger.info('App created')

    return application


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(application.config['LANGUAGES'])


application = create_app()
