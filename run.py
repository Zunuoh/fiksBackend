from flask import Flask, jsonify, request
import pymongo
import json

app = Flask(__name__)

# connect DB
try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    # trigger exception if cannot connect to db, serverSelectionTimeoutMS-time to timout if error=true
    db = mongo.company
    mongo.server_info()
except:
    print("ERROR - Cannot connect to db")

users = [{"id":1,"name":"Mary"}, {"id":2,"name":"Joseph"}, {"id":3,"name":"Anne"}]
# users=employees

nextUserId = 4

@app.route("/users", methods=["GET"])
def get_users():
    print("usersss", jsonify(users))
    return jsonify(users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id: int):
    user = get_user(id)
    if user is None:
        return jsonify({'error': 'User does not exist'})
    return jsonify(user)

def get_user(id):
    return next((e for e in users if e['id'] == id), None)

def user_is_valid(user):
    for key in user.keys():
        if key != 'name':
            return False
        return True


@app.route('/users', methods=['POST'])
def create_user():
    global nextUserId
    user = json.loads(request.data)
    if not user_is_valid(user):
        return jsonify({"Error":"Invalid user properties"}), 400   

    user['id'] = nextUserId    
    nextUserId += 1
    users.append(user) 

    return "", 201, {'location': f'/users/{user["id"]}'}

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id: int):
    user = get_user(id)
    if user is None:
        return jsonify({'error': 'User does not exist'}), 400

    updated_user = json.loads(request.data)
    if not user_is_valid(updated_user):
        return jsonify({'error': 'User does not exist'}), 400

    user.update(updated_user)

    return jsonify(user)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    global users
    user = get_user(id)
    if user is None:
        return jsonify({'error':'User does not exist'}), 404

    users = [e for e in users if e['id'] != id]
    return jsonify(user), 200

@app.route('/add', methods=['POST'])
def add_cust():
    

        



# @app.route("/users", methods=["POST"])
# def create_user():
#     try:
#         user = {
#             # "name":"dd", 
#             # "lastName":"ww"
#             "name":request.get_data("name"), 
#             "lastName":request.get_data("lastName")
            
#         }
#         print("USERRR", user)
#         # db here points to mongo.company
#         dbResponse = db.users.insert_one(user) 
#         print("RESPONSEEEEE",dbResponse.inserted_id)
#         return Response(
#             response = json.dumps(
#                 {"message":"user created", 
#                 "id":f"{dbResponse.inserted_id}"
#                 }
#             ),
#             status=200,
#             mimetype="application/json"
#         )
#         # for attr in dir(dbResponse):
#         #     print(attr)
#     except Exception as e:
#         print("******")
#         print("e")
#         print("******")

#####################
 if __name__ == "__main__":
    app.run(port=8000, debug=True)