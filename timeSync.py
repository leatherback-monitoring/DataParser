# coding: utf-8
import time, datetime
from datetime import datetime, timedelta
import csv
#import calendar
import pandas as pd
#import numpy.random as random
import sys,os

def checkResetOverflow(timeSeries):
	reset = False
	resetRows = []
	for i in range(0,len(timeSeries)):
			if i > 0:
				if timeSeries[i] < timeSeries[i-1]:
					#recursively edit overflow
					timeSeries[i] = timeSeries[i-1] + 8
					#print timeSeries[i]
					#for debugging/logging
					reset = True
					resetRows.append(i)
	if reset == True:
		for i in range(0, len(resetRows)):
			#check to see if reset is unique or is just a chain of reset/overflow
			if resetRows[i] != resetRows[i-1] + 1:
				print "edited due to overflow or reset at row " + str(resetRows[i])

def singleSync(dataframe, series):
	#obtain how many seconds elapsed 
	#print len(dataframe)
	lastReading = dataframe[series][len(dataframe)-1]
	#print lastReading
	calculatedStartDate = datetime.now()- timedelta(seconds=int(lastReading))
	#load times as timedelta
	timedeltas = pd.to_timedelta(dataframe[series],unit='s')
	columnName = str('realtime - ' + series)
	#adjust in time since epoch the starting time of the loggings
	dataframe[columnName] = calculatedStartDate + timedeltas

	#time string formatting
	dataframe[columnName] = pd.to_datetime(pd.DatetimeIndex(dataframe[columnName]).strftime('%X %D'))
	return dataframe
'''
#generate some noise
def noise():
	return random.randint(-2,2) * random.rand()

timeSeries = list(dataframe['rawTime'])
#generate a fake user-inputted start date with some error built-in (for testing time correction purposes only

for i in range (0,len(timeSeries)):
		#if i == 0:
		 #       timeSeries[i] = timeSeries[i] + noise()
		if i > 0:
				timeSeries[i] = timeSeries[i-1] + 8 + noise()

dataframe['noisytime'] = timeSeries

singleSync('noisytime')
'''
def getUserStartDate():
	while True:
		#userIn = raw_input("Type Date: mm/dd/yy: ")
		userDateInput = raw_input("enter the day the sensor was turned on and placed in the nest as mm/dd/yyyy: ")
		try:
			date = datetime.strptime(userDateInput, "%m/%d/%Y")
			#date = datetime.date(year=date.year, month = date.month, day=date.day)
		except ValueError as e:
			print "Invalid Format: {0}".format(e)
		else:
			return date

def getUserStartTime():
	while True:
		#do the biologists use 24hr time?
		userTimeInput = raw_input("enter the time the sensor was turned on and placed in the nest as 24-Hour time in the format hr:min (e.x. 16:32): ")
		try:
			time = datetime.strptime(userTimeInput + ":00", "%X")
			#time = timedelta(hours=time.hour, minutes=time.minute, seconds=0)
		except ValueError as e:
			print "Invalid Format: {0}".format(e)
		else:
			return time

#from http://code.activestate.com/recipes/577058/
def query_yes_no(question, default="yes"):
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".
	"""
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [yes/no] "
	elif default == "yes":
		prompt = " [yes/no] "
	elif default == "no":
		prompt = " [yes/no] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")

def valiDate():
	date = getUserStartDate()
	time = getUserStartTime()
	userStartDateTime = datetime(year=date.year, month=date.month, day=date.day, hour=time.hour, minute= time.minute, second=0)
	print "your date is: " + str(userStartDateTime)
	userVerify = query_yes_no("is this correct? ")
	if userVerify == False:
		valiDate()
	if userVerify == True:
		print "synchronizing time now..."
		return userStartDateTime

def DoubleSync(dataframe, series):
	columnName = str('doubleSyncRealTime - ' + series)
	#if the user start date doesn't match the singleSync start date, do I adjust by taking the
	#currentTime - userStartTime / number of readings (not preserving 8-sec logging) or by doing
	#userStartTime + 8n?

	#% will adjust syncing approach based on the percentage off the data is.
	tolerance = .1
	userStartDateTime = valiDate()
	timeElapsed = dataframe[series][len(dataframe[series])-1] - dataframe[series][0]
	if userStartDateTime - dataframe[series][0] !=0:
		percentOff = abs((userStartDateTime - dataframe[series][0])/(dataframe[series][len(dataframe[series])-1] - dataframe[series][0]))
		print str(userStartDateTime - dataframe[series][0]) + " off"
		#print str(percentOff) + " percent off"
		if percentOff > tolerance:
			#userStartTime + 8n
			dataframe['syncedTime'] = pd.date_range(freq=pd.DateOffset(seconds=8),start=userStartDateTime,periods=len(dataframe[series]))
			#for i in range(0, len(dataframe[series])-1):
			   # print userStartDateTime + timedelta(seconds=8*i)
				#dataframe['doublesync'].append(userStartDateTime + timedelta(0,0, 8*i ))
		elif percentOff < tolerance:
			#print "wow, you're actually pretty accurate"
			#interval = 8 seconds +/- some number of microseconds
			interval = (dataframe[series][len(dataframe[series])-1] - userStartDateTime)/(len(dataframe[series]) - 1)
			print str(interval) + "seconds"
			dataframe['syncedTime'] = pd.date_range(start=userStartDateTime, periods= len(dataframe[series]), freq=pd.DateOffset(seconds=interval.seconds, microseconds=interval.microseconds))
			
