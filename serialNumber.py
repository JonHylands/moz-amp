#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
import struct

print 'Mozilla Ammeter Serial Number'

if platform.system() == "Linux":
	serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
else:
	serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)

commandBytes = bytearray.fromhex("ff ff 01 02 0E EE") #GET_SERIAL

serialPort.flushInput()

serialPort.write(commandBytes)
serialPort.flush()

bytes = serialPort.read(8)
serialPort.close()

serialNumber = ord(bytes[5]) + (256 * ord(bytes[6]))

print 'Serial Number: ', serialNumber
