# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# mf first commit 48
import time
import board
import adafruit_dht
from datetime import datetime
import sys
import mariadb
from DHT_DB import *
from MF_Functions import *
import RPi.GPIO as GPIO

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)
#dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Maria database object
dbh = iDHT_DB()

# Setup GPIO for LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# variables
cError = "" # get the error string and store it in the db
#loop on getting data, storing data and blink LED 
while True:
    try:
        temperature_c = temperature_f = humidity = 0
        GPIO.output(18,GPIO.HIGH)     
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        cError = error.args[0]
        print(cError)
        time.sleep(2.0)    
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    except:
        print(error.args[0])
    else:
        temperature_f = temperature_c * (9 / 5) + 32
        
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            ) + " " + GetTimeStamp()
        )
        # Add a row of data to the database
        dbh.add_data(GetTimeStamp(), temperature_f, humidity, 2, cError)
        # Clear the error string
        cError = ""
        
        #LED goes low for a second
        GPIO.output(18,GPIO.LOW)
        time.sleep(2.0)    
        # End of While True loop
