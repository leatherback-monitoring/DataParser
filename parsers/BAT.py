import re, datetime, utils



class BAT:
	regex = re.compile(r'#BATT?:(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		millis = int(m.group(1))
		return (millis)

if __name__ == "__main__":
	parser = BAT()
	print parser.parse("hi")
	print parser.parse("#BATT:2228255,29.54,3.6804")