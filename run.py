from flask import Flask
import pymongo

app = Flask(__name__)

# connect DB
try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    # trigger exception if cannot connect to db, serverSelectionTimeoutMS-time to timout if error=true
    mongo.server_info()
except:
    print("ERROR-Cannot connect to db")



@app.route("/users", methods=["POST"])
def create_user():
    return "x"

#####################
if __name__ == "__main__":
    app.run(port=8000, debug=True)