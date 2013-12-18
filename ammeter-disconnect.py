#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import platform

# when we run from Notepad++, the working directory is wrong - fix it here
currentPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentPath)

print 'Mozilla Ammeter - Disconnect Battery Test'

if platform.system() == "Linux":
	serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
else:
	serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)

commandBytes = bytearray.fromhex("ff ff 01 02 05 F7") #TURN_OFF_BATTERY
# commandBytes = bytearray.fromhex("ff ff 01 02 06 F6") #TURN_ON_BATTERY

serialPort.write(commandBytes)
serialPort.flushInput()
serialPort.close()

print 'Battery Disconnected'
