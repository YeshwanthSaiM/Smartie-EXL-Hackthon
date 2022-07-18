# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import app

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/convert')
def convert():
    uni_path = request.args.get("json_path")
    botType = request.args.get("bot_type")
    definiton = app.convert(uni_path, botType)
    return {"response":"Success"}

 
if __name__ == '__main__':
    app.run()