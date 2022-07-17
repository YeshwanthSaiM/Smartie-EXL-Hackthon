# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import app

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/extractFromFile')
def hello_world():
    img_file_path = request.args.get("path")
    text = app.extractTextFromImg(img_file_path)
    return {"text":text}

 
if __name__ == '__main__':
    app.run()