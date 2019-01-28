import os

import logging
import peewee as pw
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from logging.handlers import SMTPHandler, RotatingFileHandler

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

    application.config['APPS'] = ['cajitos_site']
    application.config['SECRET_KEY'] = settings.SECRET_KEY
    application.config['MAIL_SERVER'] = settings.MAIL_SERVER
    application.config['MAIL_PORT'] = settings.MAIL_PORT
    # application.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
    application.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
    application.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
    application.config['PER_PAGE'] = settings.PER_PAGE
    application.config['OWNERS'] = settings.OWNERS

    bcrypt.init_app(application)
    login_manager.init_app(application)
    mail.init_app(application)

    from cajitos_site.users.routes import users
    from cajitos_site.blog_posts.routes import posts
    from cajitos_site.misc.routes import misc
    from cajitos_site.errors.routes import errors
    application.register_blueprint(users)
    application.register_blueprint(posts)
    application.register_blueprint(misc)
    application.register_blueprint(errors)

    return application


application = create_app()
if not application.debug:
    if application.config['MAIL_SERVER']:
        auth = None
        if application.config['MAIL_USERNAME'] or application.config['MAIL_PASSWORD']:
            auth = (application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD'])
        secure = None
        # if application.config['MAIL_USE_TLS']:
        #     secure = ()
        mail_handler = SMTPHandler(
            mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
            fromaddr='no-reply@' + application.config['MAIL_SERVER'],
            toaddrs=application.config['OWNERS'], subject='Cajitos Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        application.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cajitos.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        application.logger.addHandler(file_handler)
        application.logger.setLevel(logging.INFO)
        application.logger.info('Cajitos startup')
