import re, datetime, utils.parser



class Parser:
	regex = re.compile(r'#GPS:(\d+),(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return

		millis = int(m.group(1))
		return (millis)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#GPS:2136,12,37.462688,-122.274070,229.20,9,114")