#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
'''
This is the code for
    - `Grove - Sound Sensor <https://www.seeedstudio.com/Grove-Sound-Sensor-p-752.html>`_

Examples:

    .. code-block:: python

        import time
        from grove.grove_sound_sensor import GroveSoundSensor

        # connect to alalog pin 2(slot A2)
        PIN = 2

        sensor = GroveSoundSensor(PIN)

        print('Detecting sound...')
        while True:
            print('Sound value: {0}'.format(sensor.sound))
            time.sleep(.3)
'''
import math
import time
from datetime import datetime
from grove.adc import ADC
import pymongo 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy
from scipy import stats

__all__ = ['GroveSoundSensor']

uri = "mongodb+srv://CPSProject:CPSProject@cluster0.ybbw04x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Project-2']
collection = db["Sound"]

class GroveSoundSensor(object):
    '''
    Grove Sound Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def sound(self):
        '''
        Get the sound strength value

        Returns:
            (int): ratio, 0(0.0%) - 1000(100.0%)
        '''
        value = self.adc.read(self.channel)
        return value

Grove = GroveSoundSensor


def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()

    sensor = GroveSoundSensor(pin)

    print('Detecting sound...')
    soundList = []
    start_time = time.time()
    interval = 5 #5 seconds interval
    next_reset = start_time + interval
    
    while True:
        print('Sound value: {0}'.format(sensor.sound))
        print(datetime.now())
        print('========')
        soundList.append(sensor.sound)
        if time.time() >= next_reset:
            start_time = time.time()
            next_reset = start_time + interval
            # Mean Median Mode Calculation
            meanSound = numpy.mean(soundList)
            medianSound = numpy.median(soundList)
            modeSound = stats.mode(soundList)
            if meanSound != 0 and medianSound != 0 and modeSound != 0 : 
                collection.insert_one({"datetime": datetime.now(),"Mean Sound": meanSound, "Median Sound": medianSound, "Mode": modeSound})
            soundList = []
            print("data sent to MongoDB")
        #time.sleep(300)
        time.sleep(10) # for demo 
    

if __name__ == '__main__':
    main()

