#!/usr/bin/env python
# -*- coding: utf-8 -*-
#adapted from https://github.com/widakay/QuadcopterDataParser


import time
import os
import sys
#import struct
import parsers
import parsers.HTU
#import numpy
import pandas as pd
import serInput
import timeSync
import datetime
import types
import matplotlib
#import json

from operator import itemgetter




directory = os.path.join(os.path.expanduser('~'),'Documents',  "turtleSensorData", "sensors", "delete") #+ "/"  + str(int(time.time()))


if len(sys.argv) > 1:
	directory = sys.argv[1]

if not os.path.exists(directory):
	os.makedirs(directory)

raw_data = os.path.join(directory, "sensor_" + str("delete") + "-" + str(datetime.date.today()) + "-raw_data.txt")

print "opening", raw_data

#TODO: do this first to cause errors before the user enters anything
port = serInput.findPort()

dataFile = open(raw_data, "a")
if port:
	dataFile.write(serInput.readInput(port, deleteData=True))
else:
	print "using cached data"
dataFile.close()
