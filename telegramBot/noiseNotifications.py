import telebot
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from geopy.geocoders import Nominatim
import os
import datetime

#initialise data
geolocator = Nominatim(user_agent="myGeocoder")

# ===========Database Connection================
uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1')) #mongodb
try: 
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)

# ===========Telegram Bot Connection================
"""HawkerEyeBot sends the message in the Noise Notifications Telegram Channel"""
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
channel_id = '-1002123530600'

# ================Hardcoded data================
latitude = 1.29845948398373  # Hardcoded location coordinates
longitude = 103.85161150371341
location_name = ''
loc_dict = {location_name: [latitude, longitude]}

sound_threshold = 60  # decibel level
continuous_event_counter = 0
lastsent_notification_time = 0

# ================Looks for Sound collection in MongoDB================
db = client.Project
sound_db = db["Sound"].find()
collection = db["Sound"]
change_stream = collection.watch()

# ================Test code================
# location = geolocator.reverse((loc_dict[location_name][0], loc_dict[location_name][1]), exactly_one=True)
# print(location)
# bot.send_message(chat_id=channel_id, text=f"Detected sound levels over {sound_level}dB at the following location: {location}")
# bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)

for change in change_stream:
    threshold_count = 0.6 * len(change['fullDocument']['Sound'])
    if 'fullDocument' in change and 'Sound' in change['fullDocument']:
        # obtain all 60 sound values recorded over the course of 5 minutes and checks if it exceeds threshold
        exceed_threshold_count = 0
        for sound_level in change['fullDocument']['Sound']:
            if sound_level > sound_threshold:
                exceed_threshold_count += 1
        
        if exceed_threshold_count > threshold_count: # if more than 60% of the sound values of one entry is exceeded threshold
            continuous_event_counter +=1
            location = geolocator.reverse((loc_dict[location_name][0], loc_dict[location_name][1]), exactly_one=True) # Get the location name based on latitude and longitude
            location_name = location.address
            if continuous_event_counter == 1:
                bot.send_message(chat_id=channel_id, text=f"Detected sound levels over {sound_level}dB \nat the following location: {location_name}")
                bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)
                lastsent_notification_time = datetime.datetime.now()

            elif continuous_event_counter == 2 and (datetime.datetime.now() - lastsent_notification_time).total_seconds() > 600: #send second continuous event at after 15min (20 min elapsed)
                bot.send_message(chat_id=channel_id, text=f"Detected sound levels over {sound_level}dB \nat the following location: {location_name}")
                bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)
                lastsent_notification_time = datetime.datetime.now()
            
            elif continuous_event_counter == 3 and (datetime.datetime.now() - lastsent_notification_time).total_seconds() > 900:
                bot.send_message(chat_id=channel_id, text=f"Detected sound levels over {sound_level}dB \nat the following location: {location_name}")
                bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)
                lastsent_notification_time = datetime.datetime.now()
            
            elif continuous_event_counter > 4 and (datetime.datetime.now() - lastsent_notification_time).total_seconds() > 1800:
                bot.send_message(chat_id=channel_id, text=f"Detected sound levels over {sound_level}dB \nat the following location: {location_name}")
                bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)
                lastsent_notification_time = datetime.datetime.now()
        else:
            continuous_event_counter == 0