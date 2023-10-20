import Adafruit_DHT
import time
import pymongo
from datetime import datetime
from flask import Flask 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy
from scipy import stats

uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Project']
collection = db["Temperature"]

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17

start_time = time.time()
interval = 10 #30 seconds interval
next_reset = start_time + interval
temperatureList = []
humidityList = []

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    try:
        #print("Temp={0:01f}C Humidity={1:0.1f}%".format(temperature,humidity))
        print("temperature:",temperature)
        print("humidity:", humidity)
        temperatureList.append(temperature)
        humidityList.append(humidity)
        if time.time() >= next_reset:
                start_time = time.time()
                next_reset = start_time + interval

                # Mean Median Mode 
                meanTemperature = numpy.mean(temperatureList)
                medianTemperature = numpy.median(temperatureList)
                modeTemperature = stats.mode(temperatureList)
                meanHumidity = numpy.mean(humidityList)
                medianHumidity = numpy.median(humidityList)
                modeHumidity = stats.mode(humidityList)

                collection.insert_one({"datetime": datetime.now(),"meanTemperature": meanTemperature,"medianTemperature": medianTemperature, "modeTemperature": modeTemperature , "meanHumidity": meanHumidity, "medianHumidity": medianHumidity, "modeHumidity": modeHumidity})
                print("Temperature and Humdity data sent to MongoDB")
                temperatureList = []
                humidityList = []
    except RuntimeError as error:
        print(error.args[0])
    time.sleep(5)

