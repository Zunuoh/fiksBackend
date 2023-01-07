from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)

# add db config - where file should be stored
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')


@app.route('/')
def hello_world():
    return jsonify(message='Hello world!')


@app.route('/super_simple')
def super_simple():
    return jsonify(message='hii')


# creating url parameters 
@app.route('/parameters')
def parameters():
    # request.args gives access to all url variables
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry ' + name + ' you are not old enough'), 401
    else:
        return jsonify(message='Welcome ' + name + ' you are old enough!')
  
# creating url variables
@app.route('/url_variables/<string:name>/<int:age>')
# function should have same num of arguments as num in routes
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message='Sorry ' + name + ' you are not old enough'), 401
    else:
        return jsonify(message='Welcome ' + name + ' you are old enough!')


















if __name__ == "__main__":
    app.run(port=8000, debug=True)