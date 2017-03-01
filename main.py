#!/usr/bin/env python


#adapted from https://github.com/widakay/QuadcopterDataParser


import time
import os
import sys
#import struct
import parsers
import parsers.HTU
#import numpy
import pandas as pd
import serInput
import timeSync
import datetime
import types
#import json

from operator import itemgetter

sensorID = "NO_ID"

def getSensorID():
	sensorID = raw_input("enter the sensor ID: ")
	try:
		int(sensorID)
	except ValueError:
		print "%s is not a number. Please try again" % sensorID 
		return getSensorID()
	else:
		print "sensor ID validated: %d" % int(sensorID)
		return sensorID

sensorID = getSensorID()
directory = os.path.join(os.path.expanduser('~\Documents'),  "turtleSensorData", "sensors", str(sensorID)) #+ "/"  + str(int(time.time()))


if len(sys.argv) > 1:
	directory = sys.argv[1]

if not os.path.exists(directory):
	os.makedirs(directory)

raw_data = os.path.join(directory, str(datetime.date.today()) + "-raw_data.txt")

print "opening", raw_data

#TODO: do this first to cause errors before the user enters anything
port = serInput.findPort()

dataFile = open(raw_data, "a")
if port:
	dataFile.write(serInput.readInput(port, deleteData=False))
else:
	print "using cached data"
dataFile.close()

parserList = {}
for name, module in parsers.__dict__.iteritems():
	if type(module) is types.ModuleType:
		for name2, parser in module.__dict__.iteritems():
			if type(parser) is types.ClassType:
				if name2 == "Parser":
					print "adding parser:", name
					parserList[name] = parser()

# 	GPS example:
#		#GPS:2136,12,37.462688,-122.274070,229.20,9,114
#		$GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#
#		#GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126
#	IMU example:
#		#IMU:343808,25.31,-7,-7,-7,-55,118,29,956,0,16736:#

parsers.testParsers(parserList)


log = open(raw_data, "r")
fileshort = raw_data[:raw_data.find(".txt")]
print fileshort


sensorNames = {
	0:"time",
	1:"HTU"
}

	# Measure the relative humidity
	#uint16_t RH_Code = makeMeasurment(HUMD_MEASURE_NOHOLD);
	#result = (125.0*RH_Code/65536)-6

	#Measure temperature
	#uint16_t temp_Code = makeMeasurment(TEMP_MEASURE_NOHOLD);
	#result = (175.25*temp_Code/65536)-46.85

csvpath = os.path.join(directory,  str(datetime.date.today()) + "-data.csv")
#combined = open(csvpath, "w")
#combined.write("Time(ms),temperature, humidity\n")


#if not os.path.exists(csvpath):
#	os.mkdir(csvpath)

#htu = open(csvdir+sensorNames[0]+".csv", "w")
#htu.write("Time,temperature (C),humidity\n")

combined = open(csvpath, "w")
#combined.write("Time(ms),temperature, humidity\n")

lastTemp = 0
lastHumidity = 0

startTime = datetime.datetime.now()
lasttime = 0
 
def logCombined():
	combined.write(str(parser.millis) + "," + str(lastTemp) + "," + str(lastHumidity) + '\n')

print "parsing"
i=0

for line in log.readlines():
	line = line.strip()
	i += 1
	for name, parser in parserList.iteritems():    
		if parser.parse(line):
			if parser.type == "HTU":
				#print "logging"
				lastTemp = parser.temperature
				lastHumidity = parser.humidity
				#htu.write(str(parser))
				logCombined()

combined.close()
#time synchronization below:

data = pd.read_csv(str(csvpath), names = ['rawTime','temp','humidity'])

if len(data) > 0:
	#multiply to get time in seconds
	data['rawTime'] = data['rawTime']*8

	timeSeries = list(data['rawTime'])

	timeSync.checkResetOverflow(timeSeries)

	#write data back into dataframe -- can be done better
	data['rawTime'] = timeSeries

	timeSync.singleSync(data, 'rawTime')


	timeSync.DoubleSync(data, 'realtime - rawTime')

	#clean up the data with the raw output, temp, humidity, and synchronized time only.
	cleanData = data[['rawTime','temp','humidity','syncedTime']]

	pd.DataFrame.to_csv(cleanData,path_or_buf=csvpath)

	print "Time synchronized. File saved to: " + csvpath
else:
	print "No data found. Try synching again or checking file contents manually."
raw_input("press enter to exit.")