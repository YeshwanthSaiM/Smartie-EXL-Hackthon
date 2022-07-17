# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import app

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/summerize')
def summarize_():
    para = request.args.get("para")
    text = app.summarize_paragraph(para)
    return {"text":text}

 
if __name__ == '__main__':
    app.run()