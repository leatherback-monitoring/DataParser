import time
from datetime import datetime, timedelta
import csv
import pandas as pd
import numpy.random as random
import sys

sys.setrecursionlimit(20000)

data = pd.read_csv("data.csv")

#multiply to get time in seconds
data['time'] = data['time']*8
	

#for i in data['time']:
    #print Index(data['time'],i.get_loc()
timeSeries = list(data['time'])

for i in range(0,len(timeSeries)):
        if i > 0:
            if timeSeries[i] < timeSeries[i-1]:
                #recursively edit overflow
                timeSeries[i] = timeSeries[i-1] + 8
                print "edited due to overflow or reset at row " + str(i)

#write data back into dataframe
data['time'] = timeSeries

def singleSync(series):
    #obtain how many seconds elapsed 
    lastReading = data[series][len(data)-1]

    calculatedStartDate = datetime.now()- timedelta(seconds=int(lastReading))
    #load times as timedelta
    timedeltas = pd.to_timedelta(data[series],unit='s')
    columnName = str('realtime - ' + series)
    #adjust in time since epoch the starting time of the loggings
    data[columnName] = calculatedStartDate + timedeltas

    #time string formatting
    data[columnName] = pd.Series(pd.DatetimeIndex(data[columnName]).strftime('%X %D'))
    
singleSync('time')
#generate some noise
def noise():
    return random.randint(-2,2) * random.rand()

timeSeries = list(data['time'])
#generate a fake user-inputted start date with some error built-in (for testing time correction purposes only

for i in range (0,len(timeSeries)):
        #if i == 0:
         #       timeSeries[i] = timeSeries[i] + noise()
        if i > 0:
                timeSeries[i] = timeSeries[i-1] + 8 + noise()

data['noisytime'] = timeSeries

singleSync('noisytime')
data.head()    

def getUserStartDate():
    while True:
        #userIn = raw_input("Type Date: mm/dd/yy: ")
        userDateInput = raw_input("enter the day the sensor was turned on and placed in the nest as mm/dd/yyyy ")
        try:
            date = datetime.strptime(userDateInput, "%m/%d/%Y")
        except ValueError as e:
            print "Invalid Format: {0}".format(e)
        else:
        	return date
        	print date


def getUserStartTime():
    while True:
        #do the biologists use 24hr time?
        userTimeInput = raw_input("enter the time the sensor was turned on and placed in the nest as 24-Hour time in the format hr:min (e.x. 16:32): ")
        try:
            time = datetime.strptime(userTimeInput + ":00", "%X")
            time = timedelta(hours=time.hour, minutes=time.minute, seconds=0)
        except ValueError as e:
            print "Invalid Format: {0}".format(e)
    	else:
    		return time
    		print time
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
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
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

userStartDateTime = ""
def valiDate():
	userStartDateTime = getUserStartDate() + getUserStartTime()
	print "your date is: " + str(userStartDateTime)
	userVerify = query_yes_no("is this correct? ")
	if userVerify == False:
		valiDate()
	if userVerify == True:
		return "synchronizing time now..."
		#return userStartDateTime
valiDate()


#if the user start date doesn't match the singleSync start date, do I adjust by taking the
#currentTime - userStartTime / number of readings (not preserving 8-sec logging) or by doing
#userStartTime + 8n?

#% will adjust syncing approach based on the percentage off the data is.
tolerance = 10

if userStartDateTime - data['realtime - noisytime'][0] !=0:
	print "sync time off!"