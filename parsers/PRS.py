import re, datetime, utils.parser



class Parser:
	def __init__(self):
		self.type = "PRS"
		self.millis = 0
		self.temperature = 0
		self.pressure = 0

	def __str__(self):
		return str(self.millis) + "," + str(self.pressure) + "," + str(self.temperature) + '\n'

	regex = re.compile(r'#PRS:(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		
		millis = int(m.group(1))
		self.temperature = float(m.group(2))
		self.pressure = float(m.group(3))
		return (self.millis, self.pressure, self.temperature)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#PRS:182794,23.10,992.5100")