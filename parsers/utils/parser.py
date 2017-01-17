
import datetime, struct


def parseFloat(inString):
	return struct.unpack('f', inString.decode("hex"))[0]


def parseDate(date,time):
	if date<10000:
		raise Exception("Invalid Date")
	year=date%100
	if year != 15:
		year = 15
	if year>80:
		year += 1900
	else:
		year += 2000
	month = (date/100)%100
	day = date/10000
	hour = time / 1000000
	minute = (time / 10000) % 100
	second = (time / 100) % 100

	return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
