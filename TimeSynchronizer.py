import time, datetime
from datetime import timedelta
import csv
import calendar
import pandas

fi = open("data.csv")
csv_data = csv.reader(fi)

data = []
for i in csv_data:
	#if i > 0:
	print i[0]
		#print all times
		#with open("timetest.txt", "w") as writefile:
		#if row[0] < row[i-1]:
		#	print row[i] + row[i-1]
		#else:
		#print row[i]

with open("timetest.txt","r") as f:
	# read a list of lines into data
	_data = f.readlines()


def parseTime(milliseconds):
	second, milliseconds = divmod(milliseconds, 1000)
	minute, second = divmod(second, 60)
	hour, minute = divmod(minute, 60)
	day, hour = divmod(hour, 24)
	month = time.gmtime()[1] - milliseconds
	year = time.gmtime()[0] - milliseconds
	return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
print str(time.strftime('%Y %m months %d days %H:%M:%S', time.gmtime()))

#parseTime(1966)
#newformat = time.format("%Y-%m-%d %H:%M")
# now change the 2nd line, note that you have to add a newline
lastTime = 0
count = 0
seconds = 0

for i in _data:
	#converts minutes to seconds
	if int(i) > 1000:
		i = str(int(i)/1000)
		_data[count] = i+"\n"
		if int(i) < lastTime:
			newTime = 1 + lastTime
			
			_data[count] = str(newTime) + "\n"
			lastTime = newTime
		else:
			lastTime = int(i)
	count+=1

seconds = timedelta(seconds=int(_data[len(_data)-1]))
startDate = datetime.datetime.now() - seconds
print startDate
	
# and write everything back
with open("timetest.txt","w") as f:
	f.writelines(_data)