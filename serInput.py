
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
		if "usb" in port:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				print "OSError"
				pass

	print "found ports:", ports, "using port:", result
	return result

class UnknownSerialPortException(Exception):
	pass

def findPort():
	serialPorts = listSerialPorts()
	if len(serialPorts) > 0:
		port = serialPorts[0]
		return port
	return

def readInput(port, deleteData=True):
	if not os.path.exists(port):
		raise UnknownSerialPortException("Port " + port + " does not exist")
	else:
		# configure the serial connection
		ser = serial.Serial(
			port=port,
			baudrate=115200,
			parity=serial.PARITY_ODD,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.SEVENBITS
		)





		# double-check that the serial port can be connected to and buffers are empty
		# by continuing when the port is already open, this fixes some bugs on Mac OS X, but may cause problems
		# if another process has control the serial port
		if ser.isOpen():
			print "Port already open..."
		else:
			print "Opening port..."
			ser.open()

		ser.flush()
 		# Send read command
		ser.write("r")

		end = time.time() + 4
		print "reading data...."
		
		data = ""
		# Continuously read data until sensor has not replied for 4 seconds
		while time.time() < end:
			while ser.inWaiting():

				addition = ser.read(ser.inWaiting())
				data += addition
				print 'Receieved \t' + str(len(addition)) + " bytes"
				end = time.time() + 4
			time.sleep(0.5)
		print data

		if deleteData:
			print "Erasing data on device..."
			ser.write("d")
			print "Done."

		ser.close()
		return data
