import re, datetime, utils.parser
from time import ctime

class Parser:
	regex = re.compile(r'(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+)')
	def __init__(self):
		self.type = "HTU"
		self.millis = -1
		self.temperature = -1
		self.humidity = -1

	def __str__(self):
		return str(self.millis) + "," + str(self.temperature) + "," + str(self.humidity) + '\n'
	
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		
		self.millis = int(m.group(1))
		self.temperature = float(m.group(2))
		self.humidity = float(m.group(3))
		return (self.millis, self.temperature, self.humidity)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("3412302,15.40,59.60")