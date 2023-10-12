import telebot
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from telebot import types
from datetime import datetime

# initialise data

uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))  # mongodb
try:  # ping connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.Project
temp_data = db["Temperature"].find_one(sort=[("_id", -1)])
sound_data = db["Sound"].find_one(sort=[("_id", -1)])
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
all_hawker_centers = ["adam food centre", "amoy street food centre", "bedok food centre", "beo crescent market"]

print(sound_data)
print(temp_data)

sound_data = {'datetime': datetime(2023, 10, 12, 14, 29, 38, 215000), 
              'Sound': [19, 7, 1, 20, 33, 14, 33, 16, 13, 7]}

temp_data = {"temperature": [32, 34, 34, 32, 32, 33, 33, 33, 8, 4, 2, 5],
             "humidity": [60, 70, 70, 32, 32, 70, 33, 90, 78, 74, 62, 55]}


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi, which hawker center would you like to know about?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # Create a custom inline keyboard
    markup = types.InlineKeyboardMarkup()

    # Define buttons
    button1 = types.InlineKeyboardButton("Noise levels", callback_data="noise")
    button2 = types.InlineKeyboardButton("Crowd", callback_data="crowd")
    button3 = types.InlineKeyboardButton(
        "Thermal comfort", callback_data="temp")

    # Add buttons to the keyboard
    markup.add(button1, button2, button3)

    user_input = message.text.lower()
    if user_input not in all_hawker_centers:
        bot.send_message(message.chat.id, "Hawker center not recognised. Try again")
    else:
        bot.send_message(message.chat.id, "What would you like to know about?", reply_markup = markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if call.data == "noise":
        if sound_data:
             if sum(sound_data["Sound"])/len(sound_data["Sound"]) < 30:
                 bot.send_message(call.message.chat.id, "The noise level is low") #add actual value
             else:
                 bot.send_message(call.message.chat.id, "The noise level is high")
        else:
            bot.send_message(call.message.chat.id, "No data available for the given centre")
    elif call.data == "crowd":
        bot.send_message(call.message.chat.id, "You selected Crowd option")
    elif call.data == "temp":
        fan_on = True
        if temp_data:

            heat = sum(temp_data["temperature"])/len(temp_data["temperature"]) > 30 and sum(temp_data["humidity"])/len(temp_data["humidity"]) > 60
            if heat and not fan_on:
                bot.send_message(call.message.chat.id, "Thermal comfort is not ok")
            else:
                bot.send_message(call.message.chat.id, "Thermal comfort is alright")
        else:
            bot.send_message(call.message.chat.id, "No data available for the given centre")


# Start the bot
bot.polling()
