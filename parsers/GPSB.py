import re, datetime, utils.parser



class Parser:
	regex = re.compile(r'\$GPS:(\d+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		millis = int(m.group(1))
		return (millis)



if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#GPS:1329604,80415,18163100,f:E8D91542,f:4B8CF4C2,f:9A196A43,6,132")