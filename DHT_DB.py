# Module Imports
import sys
# import mariadb
from tabulate import tabulate
from datetime import datetime
from MF_Functions import *
# import io
import sqlite3

class iDHT_DB:
    def __init__(self):
        self.conn = 0
        self.curs = 0
        self.MaxRows = 0
        self.thisdict = {}
                
        try:
            self.conn = sqlite3.connect('/home/pi/Adafruit_DHT/FanData.db', check_same_thread = False)
            self.curs = self.conn.cursor()         
            # self.MaxRows = self.maxRowsTable()
            
        except Exception as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
# ------------------------------------------------------------------------------ 
 
# ------------------------------------------------------------------------------
    def print_action_tbl(self):
        sql = "SELECT * FROM fan_data"
        self.curs.execute(sql)
        myresult = self.curs.fetchall()
        print(tabulate(myresult, headers=['timestamp', 'temp', 'hum', 'speed', 'error'],tablefmt='psql'))
 # ------------------------------------------------------------------------------       
 
    def add_data(self, timestamp, temp, hum, speed, error):
        statement = "INSERT INTO fan_data (timestamp, temp, hum, speed, error) VALUES (?,?,?,?,?)"
        data = (timestamp, temp, hum, speed, error)
#    try:
#        with self.curs:
#            self.curs.execute(statement, data)
#    except Exception as e:
#        print (f"Error adding entry to databases {e}")
    self.conn.commit()
    print(timestamp + " " + str(temp) + " successfully added to database") 
# ------------------------------------------------------------------------------

# Get all rows in database and print them.
    def get_data(self):
        try:
            statement = (f"SELECT * FROM fan_data")          
            self.curs.execute(statement)
            self.conn.commit()
            # results  =  cursor.fetchall()
            # row = cursor.fetchone()
            for row in self.cursor.fetchall():
                print (row, sep=' ')        
        except Exception as e:
            print(f"Error retrieving entry from database: {e}")
# ------------------------------------------------------------------------------

# Get Max number of rows (table size)
    def maxRowsTable(self):
        for row in self.curs.execute("select COUNT(temp) from fan_data"):
            maxNumberRows=row[0]
        return maxNumberRows
# ------------------------------------------------------------------------------

# Retrieve LAST data record from database
    def getLastData(self):
        for row in self.curs.execute("SELECT * FROM fan_data ORDER BY timestamp DESC LIMIT 1"):
            time = str(row[0])
            temp = round(row[1],2) #row[1]
            hum = row[2]
        #conn.close()
        return time, temp, hum
# ------------------------------------------------------------------------------

# Get 'x' samples of historical data
    def getHistData (self, numSamples):        
        self.thisdict = {}
        for row in self.curs.execute("SELECT * FROM fan_data ORDER BY timestamp DESC LIMIT "+str(numSamples)):
            time = text_to_epoch(row[0], "%a %d%b%y %I:%M:%S %p")
            temp = round(row[1],2) #row[1]
            self.thisdict.update({time:temp})
        return self.thisdict
        
        '''
        data = self.curs.fetchall()
        dates = []
        temps = []
        hums = []
        for row in reversed(data):
            dates.append(row[0])
            temps.append(row[1])
            hums.append(row[2])
            temps, hums = self.testeData(temps, hums)
        return dates, temps, hums
        '''
# ------------------------------------------------------------------------------
# Test data for cleanning possible "out of range" values
    def testeData(self, temps, hums):
        n = len(temps)
        for i in range(0, n-1):
            if (temps[i] < -10 or temps[i] >50):
                temps[i] = temps[i-2]
            if (hums[i] < 0 or hums[i] >100):
                hums[i] = temps[i-2]
        return temps, hums

# ------------------------------------------------------------------------------
# Get Max number of rows (table size)
def maxRowsTable(self):
    for row in self.curs.execute("select COUNT(temp) from fan_data"):
        maxNumberRows=row[0]
    return maxNumberRows



# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------