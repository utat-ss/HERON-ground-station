from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from config import Config
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

functionMap = {}

with open('functions.json') as json_file:
    functions = json.load(json_file)


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def home():
    if request.method == 'GET':
        return render_template('index.html', title='Home', functions=functions)
    if request.method == 'POST':
        data = request.form
        print("Got request for function " + data["id"])
        print(data)
        return ('', 204)


if __name__ == '__main__':
    app.run()
