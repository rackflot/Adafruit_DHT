import time
import board
import adafruit_dht
from datetime import datetime
import sys
# import mariadb
from DHT_DB import *
from MF_Functions import *
import RPi.GPIO as GPIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

# Initialize the GPIO class
class iDHT_GPIO:
    def __init__(self):
        # Setup GPIO for LED
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)
        
    # Turn the LED on and off, 0x00 and 0x01    
    def LED(self, State):
        if State > 1 or State < 0:
            State = 0
        GPIO.output(18, State)
# ------------------------------------------------------------------------------
        
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
# Initial the dht device, with data pin connected to:        
class iDHT_DH:
    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT22(board.D4)
        self.Debug = False
        self.temp_f = 0
        self.temp_c = 0
        self.humidity = 0
        self.speed = 0
        self.DHT_Error = ""
    #dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    
    def ReadDHT(self):
        # variables
    #loop on getting data, storing data and blink LED 
        try:            
            GPIO.output(18,GPIO.HIGH)     
            self.temp_c     = self.dhtDevice.temperature
            self.temp_f     = self.temp_c * (9 / 5) + 32
            self.humidity   = self.dhtDevice.humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            self.DHT_Error = error.args[0]
            print(self.DHT_Error)
            time.sleep(2.0)    
        #continue
        except Exception as error:
            dhtDevice.exit()
            self.DHT_Error = error.args[0]
            raise error
        except:
            print(error.args[0])
        else:
            print("final else in ReadDHT, led OFF")
            GPIO.output(18,GPIO.HIGH)     
        
        if(self.Debug):
            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                ) + " " + GetTimeStamp()
            )
