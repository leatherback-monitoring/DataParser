import re, datetime, utils.parser



class Parser:
	regex = re.compile(r'#GPS:(\d+),(\d+),(\d+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+),(\d+),(\d+)')
	def __init__(self):
		self.type = "GPS"
		self.time = 0
		self.startTime = 0
		self.millis = 0
		self.alt = 0
		self.lat = 0
		self.lon = 0
		self.hdop = 0
		self.numSats = 0

	def __str__(self):
		return str(self.time) + "," + str(self.lat) + "," + str(self.lon) + "," + str(self.alt) + '\n'

	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		
		try:
			self.time = utils.parser.parseDate(int(m.group(2)),int(m.group(3)))
			self.startTime = self.time-datetime.timedelta(seconds=int(m.group(1))/1000.0)
		

			self.lat = utils.parser.parseFloat(m.group(5))
			self.lon = utils.parser.parseFloat(m.group(4))
			self.alt = utils.parser.parseFloat(m.group(6))
			self.numSats = int(m.group(7))
			self.hdop = int(m.group(8))

			self.millis = int(m.group(1))
			return (self.millis, self.time, (self.lat, self.lon, self.alt), self.numSats)
		except Exception as e:
			print e
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#GPS:1329604,80415,18163100,f:E8D91542,f:4B8CF4C2,f:9A196A43,6,132")