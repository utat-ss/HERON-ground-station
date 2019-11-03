from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from config import Config
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

schedules = []  # List of all schedules which will be imported

# Make list of commands that can be sent to satellite
with open('data/commands.json') as json_file:
    commands = json.load(json_file)  # List of all commands that the satellite needs to follow

# Make entire list of functions, including commands, that can be executed by schedule interpreter
with open('data/extraFunctions.txt') as function_file:
    allFunctions = function_file.readlines()  # List of all extra functions that can be scheduled
allFunctions = [line.strip() for line in allFunctions]

for command in commands:
    allFunctions.append(command['name'])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html', title='Home', commands=commands)
    if request.method == 'POST':
        data = request.form.to_dict()
        print("Got request for function " + data["id"])
        print(data)
        return ('', 204)


@app.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
    if request.method == 'GET':
        return render_template('scheduler.html', title='Scheduler', schedules=schedules, functions=allFunctions)
    if request.method == 'POST':
        data = request.form.to_dict()
        data['schedule'] = json.loads(data['schedule'])
        print("Recieved schedule")
        print(data)
        return ('', 204)


if __name__ == '__main__':
    app.run()
