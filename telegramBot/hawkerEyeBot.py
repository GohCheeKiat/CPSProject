import telebot
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from telebot import types
from datetime import datetime

# ===========Database Connection================
uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))  # mongodb
db = client.Project
try:  # ping connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)

# ===========Telegram Bot Startup================
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
print("HawkerEye Bot is up and running!")


all_hawker_centers = ["Adam Food Centre", "Amoy Street Food Centre", "Bedok Food Centre", "Beo Crescent Market"]
mean_temperature = db["Temperature"].find_one(sort=[("_id", -1)])['meanTemperature']
mean_humidity = db["Humidity"].find_one(sort=[("_id", -1)])['meanHumidity']

# ===========Telegram Sticker IDs================
cold = "CAACAgUAAxkBAAEnKL1lPNIMJUVzxKU4aik5oD4PeoC5DgACawcAAuR-eFSW1nBgAolFbzAE"
comfy = "CAACAgUAAxkBAAEnKL9lPNIuleaSlONeolg5dIl6_SYy0wACmAIAAtmQTQdeBfX7u-By7jAE"
hot = "CAACAgUAAxkBAAEnKLllPNGfdnDI62OvFATDYgABRuDWT4gAAn4FAAKZn0BVci6vdfhJSRcwBA"

def populate_hawker():
    """creates markup buttons to select hawker centers"""
    markup = types.InlineKeyboardMarkup()
    for hawkers in all_hawker_centers:
        button = types.InlineKeyboardButton(hawkers, callback_data=hawkers)
        markup.add(button)
    return markup

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to HawkerEyeBot! Please select a hawker center:", reply_markup=populate_hawker())

@bot.callback_query_handler(func=lambda call: call.message.text == "Welcome to HawkerEyeBot! Please select a hawker center:")
def handle_selection(callback_query):
    if callback_query.message.text == "Welcome to HawkerEyeBot! Please select a hawker center:":
        selection = callback_query.data
        bot.send_message(callback_query.message.chat.id, f"You selected {selection}")
        bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
        if selection == "exit": 
            exit(callback_query)
        hawker_info(callback_query)

@bot.message_handler(func=lambda msg: True)
def hawker_info(callback_query):
    markup = types.InlineKeyboardMarkup()
    option1 = types.InlineKeyboardButton("How hot is it?", callback_data="How hot is it?")
    markup.add(option1)
    bot.send_message(callback_query.message.chat.id, "What do you want to know about?", reply_markup=markup)
    if callback_query.data == "How hot is it?":
        how_hot(callback_query)

@bot.callback_query_handler(func=lambda call: call.message.text == "What do you want to know about?" or call.message.text == "What else would you like to know about?")
def how_hot(callback_query):
    selection = callback_query.data
    bot.send_message(callback_query.message.chat.id, f"You selected {selection}")
    if mean_temperature <27:
        bot.send_sticker(chat_id=callback_query.message.chat.id, sticker=cold)
    elif (mean_temperature > 28 & mean_temperature <30) & (mean_humidity >30 & mean_humidity < 50):
        bot.send_sticker(chat_id=callback_query.message.chat.id, sticker=comfy)
    else:
        bot.send_sticker(chat_id=callback_query.message.chat.id, sticker=hot)
    bot.send_message(callback_query.message.chat.id, f"Temperature: {mean_temperature}°C \nHumidity: {mean_humidity}%") 
    bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)



bot.infinity_polling()