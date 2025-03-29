import RPi.GPIO as GPIO
import time
import os


class LED_Ctrl:
    def __init__(self, iPin):
        self.LED_State = 0   
        self.iPin = iPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.iPin, GPIO.OUT)
        GPIO.output(self.iPin, GPIO.LOW)
	
        


    def LED_Action(self, action):
        if action == "on":
            GPIO.output(self.iPin, GPIO.HIGH)
            self.LED_State = 1
        if action == "off":
            GPIO.output(self.iPin, GPIO.LOW)
            self.LED_State = 0
        
    def LED_Status(self):
        # Read Sensors Status
        self.LED_State  = GPIO.input(self.iPin)
        return self.LED_State

script_directory = os.path.dirname(os.path.abspath(__file__))

mf = LED_Ctrl(18)

mf.LED_Status()    
mf.LED_Action("on")
mf.LED_Status()    

