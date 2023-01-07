from flask import Flask, jsonify, request
# import pymongo
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/super_simple')
def super_simple():
    return jsonify(message='hii')

if __name__ == "__main__":
    app.run(port=8000, debug=True)