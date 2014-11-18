#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
import struct

def ProcessPacket(packetBytes):
    packetLength = len(packetBytes)
    if packetLength != 14:
        print 'Error, got', packetLength, 'bytes, was expecting 14...'
        return (0.0, 0.0)
    dataPortion = packetBytes[5:packetLength-1]
    return struct.unpack('<ff', dataPortion)


print 'Mozilla Ammeter Calibration'

print ''

if platform.system() == "Linux":
	serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
else:
	serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)

commandBytes = bytearray.fromhex("ff ff 01 02 13 E9") #GET_CALIBRATION
serialPort.flushInput()

serialPort.write(commandBytes)
serialPort.flush()
bytes = serialPort.read(14)
serialPort.close()

values = ProcessPacket(bytes)
calibrationFloor = values[0]
calibrationScale = values[1]

print 'CalibrationFloor: {:.1f}'.format(calibrationFloor)
print 'CalibrationScale: {:.3f}'.format(calibrationScale)

