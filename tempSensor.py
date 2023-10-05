import Adafruit_DHT
import time
import pymongo
from datetime import datetime
from flask import Flask 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Project']
collection = db["Temperature"]

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:01f}C Humidity={1:0.1f}%".format(temperature,humidity))
        collection.insert_one({"datetime": datetime.now(),"temperature": temperature, "humidity": humidity})
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(2)
