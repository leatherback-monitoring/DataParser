
import re, datetime

import os, sys

'''
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
'''
def testParsers(parserList):
	testMessages = {
		"BAD":"helloasdfm,",
		"GPSA":"#GPS:2136,12,37.462688,-122.274070,229.20,9,114",
		"GPSB":"$GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#",
		"GPSC":"#GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126",
		"IMU":"#IMU:343808,25.31,-7,-7,-7,-55,118,29,956,0,16736:#",
		"PPM":"#PPM:22427,426.40,0.1365",
	}

	print "--------- Testing Parsers ---------"
	failed = False
	print "Parser".ljust(6), "Test String".ljust(12), "Result"
	for pType, parser in parserList.iteritems():
		for mType, message in testMessages.iteritems():
			m = parser.parse(message)
			if m and mType != pType:
				failed = True
				print "fail:"
				print pType.ljust(6), mType.ljust(12)+":", m
			if not m and mType == pType:
				failed = True
				print "fail:"
				print pType.ljust(6), mType.ljust(12)+":", m
			#print pType.ljust(6), mType.ljust(12)+":", m
	if not failed:
		print "All appears to be working... Yay!"
	print "-----------------------------------"
	if failed:
		sys.exit("Ensure parses are working correctly")


if __name__ == "__main__":
	parserList = {}
	print sys.modules[__name__]
	sys.exit()
	for name, module in parsers.__dict__.iteritems():
		if type(module) is types.ModuleType:
			for name2, parser in module.__dict__.iteritems():
				if type(parser) is types.ClassType:
					if name2 == "Parser":
						print "adding parser:", name
						parserList[name] = parser()
	testParsers(parserList)

# 	GPS example:
#		#GPS:2136,12,37.462688,-122.274070,229.20,9,114
#		$GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#
#		#GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126
#	IMU example:
#		#IMU:343808,25.31,-7,-7,-7,-55,118,29,956,0,16736:#
