from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/index')
def index():
    return 'Index Page'

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"