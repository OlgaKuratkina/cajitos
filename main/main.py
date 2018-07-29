from flask import Flask, render_template
application = Flask(__name__)


@application.route("/")
def hello():
    return render_template('index.html', notes=[1,2,3])


@application.route("/example")
def index():
    return 'lalalal'
