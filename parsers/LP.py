import re, datetime, utils



class Parser:
	def __init__(self):
		self.type = "LP"
		self.millis = 0
		self.LPState = 0
		self.LP = 0

	def __str__(self):
		return str(self.millis) + "," + str(self.LP) + "," + str(self.LPState) + '\n'

	regex = re.compile(r'#LP:(\d+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return

		self.millis = int(m.group(1))
		self.LPState = int(m.group(2))
		self.LP = int(m.group(3))

		return (self.millis, self.LPState, self.LP)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#LP:2229229,1,191")