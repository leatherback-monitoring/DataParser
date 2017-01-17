import re, datetime, utils



class Parser:
	def __init__(self):
		self.type = "PPM"
		self.millis = 0
		self.voltage = 0
		self.PPM = 0

	def __str__(self):
		return str(self.millis) + "," + str(self.voltage) + "," + str(self.PPM) + '\n'

	regex = re.compile(r'#PPM:(\d+),(\d+\.\d+),([-+]?\d+\.\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		self.millis = int(m.group(1))
		self.voltage = float(m.group(2)) * 3.3 / 1024
		self.PPM = float(m.group(3))
		return (self.millis, self.voltage, self.PPM)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#PPM:22427,426.40,0.1365")