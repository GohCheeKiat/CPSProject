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
# Sound after 1030pm then run 
collection = db["Humidity"]

# Define function to generate dummy data
def generate_dummy_data():
    data = {}
    data["timestamp"] = datetime.now()
    data["meanHumidity"] = str(round(random.uniform(30, 90), 1)) + "%"
    data["medianHumidity"] = str(round(random.uniform(40, 90), 1)) + "%"
    data["modeHumidity"] = str(round(random.uniform(50, 80), 1)) + "%"
    return data

# Loop through data and insert into MongoDB every minute
while True:
    now = datetime.now()
    if now >= datetime(2023, 10, 25, 0, 0, 0) and now <= datetime(2023, 10, 25, 23, 59, 59):
        data = generate_dummy_data()
        collection.insert_one(data)
        print("Inserted data")
        time.sleep(300)
