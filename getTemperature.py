#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Get Temperature
#
#  used with extended ammeter, returns probe temperature in degrees C
#

import os,sys
import serial
import time
import platform
import struct

def ProcessPacket(packetBytes):
    packetLength = len(packetBytes)
    if packetLength != 10:
        print 'Error, got', packetLength, 'bytes, was expecting 10...'
        return (0.0, 0.0)
    dataPortion = packetBytes[5:packetLength-1]
    return struct.unpack('<f', dataPortion)


print 'Mozilla Ammeter - Get Temperature'

print ''

if platform.system() == "Linux":
    serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
else:
    serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)

commandBytes = bytearray.fromhex("ff ff 01 02 1C E0") #GET_TEMPERATURE
serialPort.flushInput()
startTime = int(round(time.time() * 1000))
lastPrintTime = startTime
sampleInterval = 250

while True:
    currentTime = int(round(time.time() * 1000))
    if (currentTime - lastPrintTime) >= sampleInterval:
        serialPort.write(commandBytes)
        serialPort.flush()
        bytes = serialPort.read(10)

        values = ProcessPacket(bytes)
        temperature = values[0]

        print 'Temperature: {:.1f} C'.format(temperature)
        lastPrintTime = int(round(time.time() * 1000))

serialPort.close()
