'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__) 

# setup gpio lines
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs
ledRed = 18
# ledYlw = 19
# ledGrn = 26

#initialize GPIO status variables
ledRedSts = 0
# ledYlwSts = 0
# ledGrnSts = 0

# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
# GPIO.setup(ledYlw, GPIO.OUT) 
# GPIO.setup(ledGrn, GPIO.OUT) 

# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
# GPIO.output(ledYlw, GPIO.LOW)
# GPIO.output(ledGrn, GPIO.LOW)
	
@app.route("/")
def index():
	# Read Sensors Status
	ledRedSts = GPIO.input(ledRed)
# 	ledYlwSts = GPIO.input(ledYlw)
# 	ledGrnSts = GPIO.input(ledGrn)
	templateData = {
              'title' : 'GPIO output Status!',
              'ledRed'  : ledRedSts,
  #           'ledYlw'  : ledYlwSts,
  #           'ledGrn'  : ledGrnSts,
        }
	return render_template('index_App_GPIO.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
# 	if deviceName == 'ledYlw':
# 		actuator = ledYlw
# 	if deviceName == 'ledGrn':
# 		actuator = ledGrn
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	ledRedSts = GPIO.input(ledRed)
# 	ledYlwSts = GPIO.input(ledYlw)
# 	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {
              'ledRed'  : ledRedSts,
  #             'ledYlw'  : ledYlwSts,
  #             'ledGrn'  : ledGrnSts,
	}
	return render_template('index_App_GPIO.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)