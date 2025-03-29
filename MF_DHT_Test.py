# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# mf first commit 48
import time
import board
import adafruit_dht
from datetime import datetime
import sys
# import mariadb
from DHT_DB import *
from DHT_HW import *

from MF_Functions import *
import RPi.GPIO as GPIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)
#dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)


# Objects created
dbh     = iDHT_DB()
DHT     = iDHT_DH()
GPIO    = iDHT_GPIO()

# Functions
# ------------------------------------------------------------------------------
# Get sample frequency in minutes
def freqSample():
	times, temps, hums = dbh.getHistData (2)
	# timediff = time[1] - time[0]
#	fmt = '%Y-%m-%d %H:%M:%S'
#	fmt = '%d%m%y %H:%M:%S %p'
	fmt = "%a %d%b%y %I:%M:%S %p"
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)

# ------------------------------------------------------------------------------
# define and initialize global variables
global numSamples
numSamples = int( round(dbh.maxRowsTable()))
# numSamples = 5
if (numSamples > 101):
        numSamples = 100
    
global freqSamples
freqSamples = freqSample()

# variables
cError = "" # get the error string and store it in the db
#loop on getting data, storing data and blink LED 
dbh.print_action_tbl()

DHT.ReadDHT()
# last 2 parameters are speed and error
dbh.add_data(GetTimeStamp(), DHT.temp_f, DHT.humidity, 4, "none")

		
# main route 
@app.route("/")
def index():
	print("-|-|-|-|-|-|-|-| entering index")
	freqSamples = 5
	rangeTime = 10
	time, temp, hum = dbh.getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    print("-|-|-|-|-|-|-|-| entering my_form_post")
    global numSamples 
    global freqSamples
    global rangeTime
    # ifreqSamples = 5 #int(freqSamples.seconds)
    # rangeTime = 10 #int (request.form['rangeTime'])
    
    if (rangeTime < freqSamples):
        rangeTime = freqSamples + 1
    numSamples = int(round(rangeTime/freqSamples))
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time, temp, hum = dbh.getLastData()
    
    templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/temp')
def plot_temp():
	print("-|-|-|-|-|-|-|-| entering plot temp")
	times, temps, hums = dbh.getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/hum')
def plot_hum():
	print("-|-|-|-|-|-|-|-| entering plot hum")
	times, temps, hums = dbh.getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response
	
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=False)

