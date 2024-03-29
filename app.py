from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

app = Flask(__name__)

# add db config - where file should be stored
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
# app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
# app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]
# app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"]
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '253cbd2868988e'
app.config['MAIL_PASSWORD'] = '4baf2e09878f81'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# initialize db
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

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

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    # check if user has already logged in
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        print("JSONNNNN")
        email = request.json.get('email')
        password = request.json['password']
    else:
        print("NOT JSONNNNN")
        email = request.form['email']
        print("EMAILLL", email)
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded', access_token=access_token)
    else:
        return jsonify(message="Bad email/password"), 401

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = user.query.filter_by(email=email).first()
    if user:
        msg = Message("your planetary api password is " + user.password, sender="admin@planetary-api.com",recipients=[email] )
        mail.send(msg)
        return jsonify(message="password sent to " + email)
    else:
        return jsonify(message="That email doesnt exist")

# get planet
@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id:int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message="planet doesnt exist"), 404

# add planet
@app.route('/add_planet_details', methods=['POST'])
# @jwt_required
def add_planet_details():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message="There's already a planet by that name"), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = Planet(planet_name=planet_name, planet_type=planet_type, home_star=home_star, mass=mass, radius=radius, distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="You added a planet"), 201

# update planet
@app.route('/update_planet', methods=['PUT'])
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = request.form['mass']
        planet.radius = request.form['radius']
        planet.distance = request.form['distance']
        db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="doesnt exist")


# delete planet
@app.route('/delete_planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id:int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="deleted planet"), 202
    else:
        return jsonify(message="wasnt there"), 404










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