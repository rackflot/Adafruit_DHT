'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from led import *
from flask import Flask, render_template, request
app = Flask(__name__)

# create instance of the LED to control on pin 18
Led = LED_Ctrl(18)

# Start of Flask
@app.route("/")
def index_app_GPIO2():	# Read Sensors Status
	ledRedSts = Led.LED_Status()    
# 	ledYlwSts = GPIO.input(ledYlw)
# 	ledGrnSts = GPIO.input(ledGrn)
	templateData = {
              'title' : 'GPIO output Status!',
              'ledRed'  : ledRedSts,
#               'ledYlw'  : ledYlwSts,
#               'ledGrn'  : ledGrnSts,
        }
	return render_template('index_App_GPIO2.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	#if deviceName == 'ledRed':
	#	actuator = ledRed
# 	if deviceName == 'ledYlw':
# 		actuator = ledYlw
# 	if deviceName == 'ledGrn':
# 		actuator = ledGrn
   
	if action == "on":
		Led.LED_Action("on")
		# GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		Led.LED_Action("off")	
  		# GPIO.output(actuator, GPIO.LOW)

	ledRedSts = Led.LED_Status()    		     
	#ledRedSts = GPIO.input(ledRed)
# 	ledYlwSts = GPIO.input(ledYlw)
# 	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {
              'ledRed'  : ledRedSts,
#               'ledYlw'  : ledYlwSts,
#               'ledGrn'  : ledGrnSts,
	}
	return render_template('index_App_GPIO2.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)