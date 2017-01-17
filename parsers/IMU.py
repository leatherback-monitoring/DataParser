import re, datetime, utils



class Parser:
	def __init__(self):
		self.type = "IMU"
		self.millis = 0

	def __str__(self):
		return str(self.millis) + "," + str(self.lat) + '\n'

	regex = re.compile(r'#IMU:(\d+),([-+]?\d+\.\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		millis = int(m.group(1))
		return (millis)

