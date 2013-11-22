#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import datetime as dt
import time
import serial

SAMPLE_COUNT_PER_PACKET = 1
PACKET_SIZE = (SAMPLE_COUNT_PER_PACKET * 8) + 6

def die(msg):
    sys.exit(msg+' (check USB cable)')

def unix_time(aDate):
    epoch = dt.datetime.utcfromtimestamp(0)
    delta = aDate - epoch
    return delta.total_seconds()

def unix_time_millis(aDate):
    return unix_time(aDate) * 1000.0

class CurrentSample:
	def __init__(self, currentValue, voltageValue, msCounterValue):
		self.current = currentValue
		self.voltage = voltageValue
		self.msCounter = msCounterValue
	def getCurrent(self):
		return self.current
	def getVoltage(self):
		return self.voltage


def ProcessPacket(packetBytes):
	packetLength = len(packetBytes)
#	if packetLength != 86:
#		print 'Packet is not 86 bytes long - {} bytes'.format(packetLength)
#		return 

	headerByte = ord(packetBytes[0])
	if headerByte != 255:
		print '1st Packet header byte not 255: {}'.format(headerByte)
		return None

	headerByte = ord(packetBytes[1])
	if headerByte != 255:
		print '2nd Packet header byte not 255: {}'.format(headerByte)
		return None

	dataPortion = packetBytes[5:packetLength-1]
	dataCount = len(dataPortion) / 8
	averageCurrent = 0.0
	averageVoltage = 0.0
	startMsCounter = -1
	for index in range(0, dataCount):
		startIndex = index * 8
		endIndex = startIndex + 8
		sampleBytes = dataPortion[startIndex:endIndex]
		current = ord(sampleBytes[0]) + (ord(sampleBytes[1]) * 256)
		if (current > 32767):
			current = (65536 - current) * -1;
		voltage = ord(sampleBytes[2]) + (ord(sampleBytes[3]) * 256)
		msCounter = ord(sampleBytes[4]) + (ord(sampleBytes[5]) * 256) + (ord(sampleBytes[6]) * 65536) + (ord(sampleBytes[7]) * 16777216)
		if startMsCounter < 0:
			startMsCounter = msCounter
		averageCurrent = averageCurrent + current
		averageVoltage = averageVoltage + voltage
	averageCurrent = int(averageCurrent / dataCount)
	averageVoltage = int(averageVoltage / dataCount)
	return CurrentSample(averageCurrent, averageVoltage, startMsCounter)



class CurrentModule:
	def __init__(self):
		self.serialPort = None
		self.startMillis = None
		self.startRunning()

	def getSample(self):
		if self.serialPort.isOpen():
			commandBytes = bytearray.fromhex("ff ff 01 02 07 F5") #SEND_SAMPLE
			self.serialPort.write(commandBytes)
			bytes = self.serialPort.read(PACKET_SIZE)
			return ProcessPacket(bytes)
		else:
			return None

	def startMilliseconds(self):
		return self.startMillis

	def resyncPacket(self):
		bytes = self.serialPort.read(PACKET_SIZE * 2)
		foundHeader = False
		reachedEnd = False
		index = 0
		while not (foundHeader or reachedEnd):
			byte = ord(bytes[index])
			print 'resync: byte[{}] = {}'.format(index, byte)
			if byte == 255:
				byte = ord(bytes[index + 1])
				if byte == 255:
					packetLength = ord(bytes[index + 3])
					if packetLength == (PACKET_SIZE - 4):
						foundHeader = True
			if not foundHeader:
				index = index + 1
				if index > PACKET_SIZE:
					reachedEnd = True
		if reachedEnd:
			return False
		# now we read index bytes, which should re-align the serial port with packet boundaries
		self.serialPort.read(index)
		return True


	def stopRunning(self):
#		commandBytes = bytearray.fromhex("ff ff 01 02 03 F9") #STOP_ASYNC
#		self.serialPort.write(commandBytes)
#		self.serialPort.flush()
#		count = self.serialPort.inWaiting()
#		if count > 0:
#			junk = self.serialPort.read(count)
#		self.serialPort.flushInput()
		self.serialPort.close()
		

	def startRunning(self):
		if (self.serialPort is None) or (self.serialPort.isOpen() == False):
			self.serialPort = serial.Serial(port='COM7', baudrate=1000000, timeout=1)
#		self.serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
#		commandBytes = bytearray.fromhex("ff ff 01 02 02 FA") #START_ASYNC
		commandBytes = bytearray.fromhex("ff ff 01 02 05 F7") #TURN_OFF_BATTERY
		commandBytes = bytearray.fromhex("ff ff 01 02 06 F6") #TURN_ON_BATTERY
		self.serialPort.flushInput()
		self.serialPort.write(commandBytes)
		self.serialPort.flush()
		self.startMillis = unix_time_millis(dt.datetime.utcnow())
