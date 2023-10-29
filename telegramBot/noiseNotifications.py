import telebot
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from geopy.geocoders import Nominatim
import os

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
sound_level = 10
latitude = 1.29845948398373  # Hardcoded location coordinates
longitude = 103.85161150371341
location_name = ''
loc_dict = {location_name: [latitude, longitude]}
threshold = 50  # percentage
count_events = 0

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
    print(change)
    if 'fullDocument' in change and 'Sound' in change['fullDocument']:
        #Sound_level = change['fullDocument']['Sound']
        sound_agg = (
            sum(1 for value in change['fullDocument']['Sound'] if value > sound_level) / len(change['fullDocument']['Sound'])) * 100
        if sound_agg > threshold:
            count_events += 1
        else:
            count_events = 0  # reset events

        if count_events == 1:
            """Get the location name based on latitude and longitude"""
            location = geolocator.reverse((loc_dict[location_name][0], loc_dict[location_name][1]), exactly_one=True)
            if location:
                location_name = location.address
                bot.send_message(chat_id=channel_id, text=f"Detected sound levels over {sound_level}dB \nat the following location: {location_name}")
                bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)

        elif count_events == 10 :
            """Get the location name based on latitude and longitude"""
            location = geolocator.reverse((loc_dict[location_name][0], loc_dict[location_name][1]), exactly_one=True)
            if location:
                location_name = location.address
                bot.send_message(chat_id=channel_id, text=f"Reminder to check on high sound levels prolonging 1 min 30 seconds at the following location: {location_name}")
                bot.send_location(chat_id=channel_id,latitude=latitude, longitude=longitude)