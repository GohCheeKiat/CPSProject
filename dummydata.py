import pymongo
from datetime import datetime
import time
import random
from statistics import mean, median, mode
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

# Connect to MongoDB database
uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Project']
collection = db["Sound"]

# Define function to generate dummy data
def generate_dummy_data():
    data = {}
    data["timestamp"] = datetime.now()
    data["meanSound"] = round(random.uniform(0, 150), 2)
    data["medianSound"] = round(random.uniform(30, 80), 2)
    data["modeSound"] = round(random.uniform(20, 50), 2)
    return data

print(generate_dummy_data())

# Loop through data and insert into MongoDB every minute
while True:
    now = datetime.datetime.now()
    if now >= datetime.datetime(2023, 10, 20, 0, 0, 0) and now <= datetime.datetime(2023, 10, 20, 23, 59, 59):
        data = generate_dummy_data()
        collection.insert_one(data)
        time.sleep(60)
    else:
        break

# Close connection to MongoDB
# client.close()
