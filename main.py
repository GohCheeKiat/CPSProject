import pymongo 
from flask import Flask 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://CPSProject:<password>@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

app = Flask(__name__)

db = client['Project']
collection = db["Thermal"]
 
@app.route("/home", methods=["GET"])
def home(): 
    collection.insert_one({'_id': '12345', 'name': 'peter'})
    return "hi"

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5000, debug=True)

