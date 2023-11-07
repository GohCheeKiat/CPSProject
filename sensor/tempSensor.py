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
db = client['Project-2']
collection = db["Temp"]

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
        if temperature == None: 
            temperature = 0 
        if humidity == None: 
            humidity = 0

        temperatureList.append(temperature)
        humidityList.append(humidity)
        if time.time() >= next_reset:
                start_time = time.time()
                next_reset = start_time + interval

                # Mean Median Mode 
                meanTemperature = round(numpy.mean(temperatureList),1) 
                medianTemperature = round(numpy.median(temperatureList),1) 
                modeTemperature = stats.mode(temperatureList).mode 
                meanHumidity = round(numpy.mean(humidityList),1) 
                medianHumidity = round(numpy.median(humidityList),1) 
                modeHumidity = stats.mode(humidityList).mode 

                sample_data_temperature = {
                    "datetime": datetime.now(),
                    "meanTemperature": int(meanTemperature) if meanTemperature is not None else None,
                    "medianTemperature": int(medianTemperature) if medianTemperature is not None else None,
                    "modeTemperature": int(modeTemperature) if modeTemperature is not None else None,
                    "meanHumidity": int(meanTemperature) if meanTemperature is not None else None,
                    "medianHumidity": int(medianTemperature) if medianTemperature is not None else None,
                    "modeHumidity": int(modeTemperature) if modeTemperature is not None else None
                }

                # sample_data_humidity = {
                #     "datetime": datetime.now(),
                #     "meanHumidity": int(meanTemperature) if meanTemperature is not None else None,
                #     "medianHumidity": int(medianTemperature) if medianTemperature is not None else None,
                #     "modeHumidity": int(modeTemperature) if modeTemperature is not None else None
                # }


                collection.insert_one(sample_data_temperature)
                #db["Humidity"].insert_one(sample_data_humidity)
                print("Temperature and Humdity data sent to MongoDB")
                temperatureList = []
                humidityList = []
        
    except RuntimeError as error:
        print(error.args[0])
    time.sleep(600)

