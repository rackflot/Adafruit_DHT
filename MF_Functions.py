
import string 
import os
import sys
import struct
import time
import psutil
from datetime import datetime
# from multipledispatch import dispatch 

# ---------------------------------------------------------------------
# Time Functions
# ---------------------------------------------------------------------

def GetTimeStamp():
    # timestamp = 1528797322
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.strftime("%a %d%b%y %I:%M:%S %p")    

#def GetDHTDate
# Return CPU temperature as a character string                                      
def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
	p = os.popen('free')
	i = 0
	while 1:
		i = i + 1
		RAM_stats = p.readline()
		if i==2:
			# return(line.split()[1:4])
			return(RAM_stats.split()[1:4])
	 #       break
	#sRAM_Stat = str(round(int(RAM_stats[0]) / 1000,1)) + str(round(int(RAM_stats[1]) / 1000,1) + str(round(int(RAM_stats[2]) / 1000,1)))
			
def getRAMInfoStr():
	p = os.popen('free')
	i = 0
	while 1:
		i = i + 1
		RAM_stats = p.readline() 
		if i==2:
			# return(RAM_stats.split()[1:4])
			RAM_stats = RAM_stats.split()[1:4]
			RAM_total = round(int(RAM_stats[0]) / 1000,1)
			RAM_used = round(int(RAM_stats[1]) / 1000,1)
			RAM_free = round(int(RAM_stats[2]) / 1000,1)
			# return("RAM Used: " + str(RAM_used) + ", RAM Free: " + str(RAM_free) + ", RAM Total: " + str(RAM_total))
			return("RAM Used: " + str(round(int(RAM_stats[1]) / 1000,1)) + ", RAM Free: "  + str(round(int(RAM_stats[2]) / 1000,1)) +  ", RAM Total: " + str(round(int(RAM_stats[0]) / 1000,1)))


# Return % of CPU used by user as a character string                                
def getCPUuse():
	return(str(os.popen("top -n1 | awk '/%Cpu\(s\):/ {print $2}'").readline().strip()))
	

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
	p = os.popen("df -h /")
	i = 0
	while 1:
		i = i +1
		line = p.readline()
		if i==2:
			return(line.split()[1:5])
 


if __name__ == '__main__':

	
	# CPU informatiom
	CPU_temp = getCPUtemperature()
	CPU_usage = getCPUuse()
	print("CPU Temp: " + CPU_temp + ", CPU Usage: "+ CPU_usage)
	# RAM information
	# Output is in kb, here I convert it in Mb for readability
	RAM_stats = getRAMinfo()
	RAM_total = round(int(RAM_stats[0]) / 1000,1)
	RAM_used = round(int(RAM_stats[1]) / 1000,1)
	RAM_free = round(int(RAM_stats[2]) / 1000,1)
	print ("RAM Used: " + str(RAM_used) + ", RAM Free: " + str(RAM_free) + ", RAM Total: " + str(RAM_total))
	# Disk information
	DISK_stats = getDiskSpace()
	DISK_total = DISK_stats[0]
	DISK_free = DISK_stats[1]
	DISK_perc = DISK_stats[3]
	print("Disk Used: " + DISK_perc + ", Disk Free: " + DISK_free + ", Disk Total: " + DISK_total)
	fEppochTime = time.time()
	print("epoctime: "+ str(fEppochTime))
	print(time.ctime(fEppochTime))
	print("GetTimeStamp():" + GetTimeStamp())
	print("--------------------------------------------------------------")
	