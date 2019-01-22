import peewee as pw
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import cajitos_site.settings as settings

db = pw.PostgresqlDatabase(
    settings.DB_NAME,
    user=settings.DB_USER,
    host=settings.DB_HOST, port=settings.DB_PORT, password=settings.DB_PASS)

bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app():
    application = Flask(__name__)

    application.config['SECRET_KEY'] = settings.SECRET_KEY
    application.config['MAIL_SERVER'] = settings.MAIL_SERVER
    application.config['MAIL_PORT'] = settings.MAIL_PORT
    application.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
    application.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
    application.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
    application.config['PER_PAGE'] = settings.PER_PAGE

    bcrypt.init_app(application)
    login_manager.init_app(application)
    mail.init_app(application)

    from cajitos_site.users.routes import users
    from cajitos_site.posts.routes import posts
    from cajitos_site.misc.routes import misc
    from cajitos_site.errors.routes import errors
    application.register_blueprint(users)
    application.register_blueprint(posts)
    application.register_blueprint(misc)
    application.register_blueprint(errors)

    return application

