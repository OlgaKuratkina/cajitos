import peewee as pw
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from cajitos_site.settings import *

application = Flask(__name__)
application.config['SECRET_KEY'] = SECRET_KEY
application.config['MAIL_SERVER'] = MAIL_SERVER
application.config['MAIL_PORT'] = MAIL_PORT
application.config['MAIL_USE_TLS'] = MAIL_USE_TLS
application.config['MAIL_USERNAME'] = MAIL_USERNAME
application.config['MAIL_PASSWORD'] = MAIL_PASSWORD

db = pw.PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    host=DB_HOST, port=DB_PORT, password=DB_PASS)

bcrypt = Bcrypt(application)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(application)

from cajitos_site import routes

