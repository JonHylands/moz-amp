#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
import struct

print 'Mozilla Ammeter Serial Number Setter'

print ''
serialNumberString = raw_input("Enter serial number: ")

serialNumber = int(serialNumberString)

print '\nSerial Number: ', serialNumber

if platform.system() == "Linux":
	serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
else:
	serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)

commandBytes = bytearray.fromhex("ff ff 01 04 0D") #SET_SERIAL
commandBytes += struct.pack("<H", serialNumber)

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
print "Serial Number sent."
