# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import app

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/recommendProduct')
def hello_world():
    product = request.args.get("product")
    text = app.getRecommendProducts(product)
    return {"text":text}

 
if __name__ == '__main__':
    app.run()