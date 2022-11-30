from flask import Flask
import pymongo

app = Flask(__name__)

# connect DB
# try:

# except:




@app.route("/users", methods=["POST"])
def create_user():
    return "x"

#####################
if __name__ == "__main__":
    app.run(port=8000, debug=True)