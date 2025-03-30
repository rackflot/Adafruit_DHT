
# Module Imports
# import sys
# from tabulate import tabulate
# import io
import sqlite3
from datetime import datetime
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import io
from DHT_DB import *
from DHT_HW import *
from MF_Functions import *
import RPi.GPIO as GPIO
from flask import Flask, render_template, jsonify

app = Flask(__name__)  

# Objects created
dbh     = iDHT_DB()
DHT     = iDHT_DH()
GPIO    = iDHT_GPIO()

#Get first Temp reading
DHT.ReadDHT()
# last 2 parameters are speed and error
# adding the last data rec
dbh.add_data(GetTimeStamp(), DHT.temp_f, DHT.humidity, 4, "none")

# get the last 5 records from the db
dbh.getHistData(5)

'''
#conn = sqlite3.connect('/home/pi/Adafruit_DHT/FanData.db', check_same_thread = False)
#curs = conn.cursor()         

thisdict = {}
for row in curs.execute("SELECT * FROM fan_data ORDER BY timestamp DESC LIMIT 5"):
    time = dbh.text_to_epoch(row[0], "%a %d%b%y %I:%M:%S %p")
    temp = round(row[1],2) #row[1]
    thisdict.update({time:temp})
    
    # hum = row[2]
#conn.close()
'''

@app.route('/')  
def chartwithXY():    
    print("-*-*-*-* Index ")
    # dbh.getHistData(5)
    #data = { "Sun 02Mar25 04:39:10 PM": 30, "Sun 02Mar25 04:39:10 PM": 40} #, 30: 50, 40:70, 50: 80 }  
    #data = { 1088620200000: 30, 1104517800000: 40} #, 30: 50, 40:70, 50: 80 }  
    #data = { 10: 30, 20: 40} #, 30: 50, 40:70, 50: 80 }  
    return render_template('index.html',data=dbh.thisdict) 

@app.route("/get_cart_rate")
def get_cart_rate():
    print("-*-*-*-* Enter get cart rate ")
    #Get first Temp reading
    DHT.ReadDHT()
    # last 2 parameters are speed and error
    # adding the last data rec
    dbh.add_data(GetTimeStamp(), DHT.temp_f, DHT.humidity, 4, "none")
    #get the last 5 records, will be in class structure thisdict
    dbh.getHistData(20)
    '''
    thisdict = {}
    for row in curs.execute("SELECT * FROM fan_data ORDER BY timestamp DESC LIMIT 5"):
        time = text_to_epoch(row[0], "%a %d%b%y %I:%M:%S %p")
        temp = round(row[1],2) #row[1]
        thisdict.update({time:temp})
        
    # index = []
    # data = {}
    # for i in rv:
    # index.append(i)
    '''
    #for key, value in index:
    #data[key] = data.get(key, 0) + value
    return jsonify(dbh.thisdict)


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5001, debug=False)  
