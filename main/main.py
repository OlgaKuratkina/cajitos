from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html', notes=[1,2,3])


@app.route("/example")
def index():
    return 'lalalal'
