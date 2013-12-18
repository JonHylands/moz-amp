#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
import struct

# when we run from Notepad++, the working directory is wrong - fix it here
currentPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentPath)

from Tkinter import *


def ProcessPacket(packetBytes):
	packetLength = len(packetBytes)
#	if packetLength != 86:
#		print 'Packet is not 86 bytes long - {} bytes'.format(packetLength)
#		return

	global PacketCount
	global CurrentTotal
	global MinCurrent
	global MaxCurrent

	dataPortion = packetBytes[5:packetLength-1]
	dataCount = len(dataPortion) / 8
	for index in range(0, dataCount):
		startIndex = index * 8
		endIndex = startIndex + 8
		sampleBytes = dataPortion[startIndex:endIndex]
		current = ord(sampleBytes[0]) + (ord(sampleBytes[1]) * 256)
		if (current > 32767):
			current = (65536 - current) * -1;
		voltage = ord(sampleBytes[2]) + (ord(sampleBytes[3]) * 256)
		msCounter = ord(sampleBytes[4]) + (ord(sampleBytes[5]) * 256) + (ord(sampleBytes[6]) * 65536) + (ord(sampleBytes[7]) * 16777216)
		print 'Sample %(index)d  - current: %(current)d voltage: %(voltage)d msCounter: %(counter)d' \
			% {"index": index, "current": current, "voltage": voltage, "counter": msCounter}
		PacketCount = PacketCount + 1
		CurrentTotal = CurrentTotal + current
		if current < MinCurrent:
			MinCurrent = current
		if current > MaxCurrent:
			MaxCurrent = current

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
