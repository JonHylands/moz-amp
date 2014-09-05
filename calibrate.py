#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
import struct

print 'Mozilla Ammeter Calibration'

print ''
calibrationFloorString = raw_input("Enter calibration floor value: ")
calibrationScaleString = raw_input("Enter calibration scale value: ")

calibrationFloor = float(calibrationFloorString)
calibrationScale = float(calibrationScaleString)

print '\nFloor: ', calibrationFloor, '\nScale: ', calibrationScale

answer = raw_input("\nType Y to calibrate with these values: ")
if (answer == "Y") | (answer == "y"):

	if platform.system() == "Linux":
		serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
	else:
		serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)

	commandBytes = bytearray.fromhex("ff ff 01 0A 09") #SET_CALIBRATION
	commandBytes += struct.pack("<f", calibrationFloor)
	commandBytes += struct.pack("<f", calibrationScale)
	
	crc = 0
	for index in range(2, len(commandBytes)):
		crc += commandBytes[index]
		print 'Byte ', index, ' = ', commandBytes[index]
	crc = 255 - (crc % 256)
	print 'CRC: ', crc
	commandBytes += struct.pack("<B", crc)

	serialPort.flushInput()

	serialPort.write(commandBytes)
	serialPort.flush()

	serialPort.close()
	print "Calibration sent."
else:
	print "Calibration cancelled."
