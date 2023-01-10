from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow


app = Flask(__name__)

# add db config - where file should be stored
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

# initialize db
db = SQLAlchemy(app)
ma = Marshmallow(app)

# create db
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DATABASE CREATED')

# destroy db
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DATABASE DROPPED')

# seed db(add test data)
@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury', 
                    planet_type='Class D', 
                    home_star='Sol', 
                    mass=3.258e23, 
                    radius=1516, 
                    distance=35.98)

    venus = Planet(planet_name='Venus', 
                    planet_type='Class K', 
                    home_star='Sol', 
                    mass=4.867e24, 
                    radius=3760, 
                    distance=67.24e6)

    earth = Planet(planet_name='Earth', 
                    planet_type='Class M', 
                    home_star='Sol', 
                    mass=5.972e2, 
                    radius=3959, 
                    distance=92.96e6)
    
    # add to db as records
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    

    test_user = User(first_name='William', 
                    last_name='Herschel', 
                    email='test@test.com', 
                    password='P@ssw0rd')

    db.session.add(test_user)
    # commit saves the changes
    db.session.commit()
    print("DATABASE SEEDED")
    



# routes
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

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)

# creating database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password= Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key = True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)


















if __name__ == "__main__":
    app.run(port=8000, debug=True)