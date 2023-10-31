import tkinter as tk
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from PIL import Image, ImageTk

# Connect to MongoDB
uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Project']
collection = db["Temperature"]

def update_fan_state():
    # Fetch the latest temperature and humidity data
    latest_data_temp = collection.find_one(sort=[('_id', -1)])
    latest_data_humidity = db["Humidity"].find_one(sort=[('_id', -1)])

    if latest_data_temp and latest_data_humidity:
        temperature = latest_data_temp['meanTemperature']
        humidity = latest_data_humidity['meanHumidity']
        print("LATEST TEMP", temperature)
        print("LATEST HUMID", humidity)
        # Determine fan state based on thresholds
        if temperature > temperature_threshold and humidity > humidity_threshold:
            update_fan_image(True)
            fan_label.config(text="Fan Spinning")
        else:
            update_fan_image(False)
            fan_label.config(text="Fan Stopped")
    else:
        fan_label.config(text="No data available")

def update_fan_image(is_spinning):
    if is_spinning:
        fan_image_label.config(image=fan_image_spinning)
    else:
        fan_image_label.config(image=fan_image_stopped)


# Define temperature and humidity thresholds
temperature_threshold = 10  # Adjust as needed
humidity_threshold = 10  # Adjust as needed

# Create the GUI
root = tk.Tk()
root.title("Fan Control")

fan_label = tk.Label(root, text="", font=("Arial", 20))
fan_label.pack()

stopped_fan = "./gif/fan-off-image.jpg"
spinning_fan = "./gif/fan-spinning.gif"

# Open and convert the images using PIL
fan_image_stopped = Image.open(stopped_fan)
fan_image_spinning = Image.open(spinning_fan)

# Convert PIL images to Tkinter PhotoImage
fan_image_stopped = ImageTk.PhotoImage(fan_image_stopped)
fan_image_spinning = ImageTk.PhotoImage(fan_image_spinning)

fan_image_label = tk.Label(root, image=fan_image_stopped)
fan_image_label.pack()

update_fan_state()  # Initial fan state update

root.after(5000, update_fan_state)  # Update fan state every 5 seconds (adjust as needed)

root.mainloop()
