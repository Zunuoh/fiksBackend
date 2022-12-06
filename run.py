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

users = [{"id":1,"name":"Mary"}]

nextEmployeeId = 4

@app.route("/users", methods=["POST"])
def create_user():
    print("usersss", jsonify(users))
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    print("usersss", jsonify(users))
    return jsonify(users)
        


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