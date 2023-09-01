from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/another")
def hello_world():
    return "<p>Hello, World!</p>"

def run():
    app.run()

