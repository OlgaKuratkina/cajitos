from flask import Flask
import peewee as pw
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from cajitos_site.settings import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASS

application = Flask(__name__)
application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

db = pw.PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    host=DB_HOST, port=DB_PORT, password=DB_PASS)

bcrypt = Bcrypt(application)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from cajitos_site import routes
