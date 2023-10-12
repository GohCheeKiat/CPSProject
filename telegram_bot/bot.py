import os
import telebot
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from geopy.geocoders import Nominatim

# customer facing - for how noisy
# seperate channel for sound - bot to be invited into channel 

# send sound and temp
# if arudino then add thermal

# Initialize the Geocoder
geolocator = Nominatim(user_agent="myGeocoder")


#mongodb connection 
uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.Project
temperature = db["Temperature"].find() #empty search query
collection = db["Sound"]

#tele bot connection 
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
channel_id = '-1001862115225'

# Sends sound and location information to channel to alert the authorities 
# Create a change stream to monitor the collection for changes
# change_stream = collection.watch()

# for change in change_stream:
#     if 'fullDocument' in change and 'Sound' in change['fullDocument']:
        # Sound_level = change['fullDocument']['Sound']
Sound_level = 31
# Hardcoded location coordinates
latitude = 1.29845948398373
longitude = 103.85161150371341
location_name = ''

if Sound_level > 30:
    message = f"Current sound level is {Sound_level}dB"
    bot.send_message(chat_id=channel_id, text=message)

    # Get the location name based on latitude and longitude
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        location_name = location.address
        bot.send_location(chat_id=channel_id, latitude=latitude, longitude=longitude)
        bot.send_message(chat_id=channel_id, text=f"Location: {location_name}")


# add db.watch() to fetch new results
# sample - with db.watch([{"$match": {"operationType": "insert"}}]) as stream:

# if temperature:
#     for pair in temperature:
#         temp = pair['temperature']
#         humidity = pair['humidity']
        
#         if humidity < 15:
#             message = "Current humidity is below 15"
#             bot.send_message(chat_id=channel_id, text=message)



# message = "Hello, this is a message from your bot!"
# bot.send_message(chat_id=channel_id, text=message)


# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")


# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


#bot.infinity_polling()


