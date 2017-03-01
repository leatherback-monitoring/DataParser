#!/usr/bin/env python

import time, serial, glob, sys, os


def listSerialPorts():

	if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this is to exclude your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')

	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')

	elif sys.platform.startswith('win'):
		ports = ['COM' + str(i + 1) for i in range(256)]

	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			#print "OSError"
			pass

	print "discovering ports...", "possible ports:", result
	return result

class UnknownSerialPortException(Exception):
	pass

def findPort():
	serialPorts = listSerialPorts()

	# *-nix
	if not sys.platform.startswith('win'):
		serialPorts = [port for port in serialPorts if "usb" in port]

	if len(serialPorts) > 0:
		port = serialPorts[0]
		print "using port", port
		return port
	return

def readInput(port, deleteData=True, ser_timeout=4):
	#if not os.path.exists(port):
	if False:
		raise UnknownSerialPortException("Port " + port + " does not exist")
	else:
		# configure the serial connection
		ser = serial.Serial(
			port=port,
			baudrate=115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)

		# double-check that the serial port can be connected to and buffers are empty
		# by continuing when the port is already open, this fixes some bugs on Mac OS X, but may cause problems
		# if another process has control the serial port
		if ser.isOpen():
			print "Port already open... If the download fails, try plugging in the sensor again"
		else:
			print "Opening port..."
			ser.open()

		ser.flush()

 		
		end = time.time() + ser_timeout
		print "reading data...."
		
		data = ""
		# Continuously read data until sensor has not replied for 4 seconds
		while time.time() < end:
			while ser.inWaiting():
				waiting = ser.inWaiting()
				data += ser.read(waiting)
				print 'Receieved \t' + str(waiting) + " bytes"
				if "Waiting" in data[-waiting:]:
					ser.write("r")
					print "Sensor booted. Fetching data..."
				end = time.time() + ser_timeout
			time.sleep(0.5)
		print "-"*10 + " Data " + "-"*10
		print data
		print "-"*27

		if deleteData:
			print "Erasing data on device..."
			ser.write("e")
			print "Done."

		ser.close()
		return data
