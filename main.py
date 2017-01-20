#!/usr/bin/env python


#adapted from https://github.com/widakay/QuadcopterDataParser


import time
import os
import sys
import datetime
import struct
import parsers
import serInput
import inspect
import simplekml
import types
import json

from operator import itemgetter



def getSensorID():
	sensorID = raw_input("enter the sensor ID: ")
	try:
		int(sensorID)
	except ValueError:
		print "%s is not a number. Please try again" %sensorID 
		getSensorID()
	else:
		print "sensor ID validated: %d" % int(sensorID)
		return sensorID


directory = "data/sensors/" + getSensorID() #+ "/"  + str(int(time.time()))
#directory = "data/" + "lowPressure" #+ str(int(time.time()))
#directory = "data/oregon/" + "baseline"


if len(sys.argv) > 1:
	directory = sys.argv[1]

if not os.path.exists(directory):
	os.makedirs(directory)

filename = directory + "/data.txt"


print "opening", filename

port = serInput.findPort()

dataFile = open(filename, "a")
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


log = open(filename, "r")
fileshort = filename[:filename.find(".txt")]
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

csvdir = directory+"/csv/"


if not os.path.exists(csvdir):
	os.mkdir(csvdir)

htu = open(csvdir+sensorNames[0]+".csv", "w")
htu.write("Time,temperature (C),humidity\n")

combined = open(csvdir+"combined.csv", "w")
combined.write("Time(ms),temperature, humidity\n")

csvdir = directory+"/csv/"

if not os.path.exists(csvdir):
	os.mkdir(csvdir)

lastTemp = 0
lastHumidity = 0

startTime = datetime.datetime.now()
lasttime = 0
 
def logCombined():
	combined.write(str(parser.millis) + "," + str(lastTemp) + "," + str(lastHumidity) + '\n')

i=0
for line in log.readlines():
	line = line.strip()
	i += 1
	for name, parser in parserList.iteritems():    
		if parser.parse(line):
			if parser.type == "HTU":
				lastTemp = parser.temperature
				lastHumidity = parser.humidity
				htu.write(str(parser))
				logCombined()
			else:
				print "error parsing: " + line

