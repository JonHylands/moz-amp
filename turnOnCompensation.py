
import sys
import serial
import struct

print ''
baselineVoltageString = raw_input("Enter baseline voltage value (3.7 - 4.2): ")

baselineVoltage = float(baselineVoltageString)

if baselineVoltage < 3.7 or baselineVoltage > 4.2:
	print 'Error - baseline voltage must be between 3.7 and 4.2 (inclusive)...'
	sys.exit(1)

print '\nBaseline Voltage: ', baselineVoltage

answer = raw_input("\nType Y to turn on compensation with this baseline: ")
if (answer == "Y") | (answer == "y"):

	serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)

	commandBytes = bytearray.fromhex("ff ff 01 06 11") #TURN_ON_COMPENSATION
	commandBytes += struct.pack("<f", baselineVoltage)

	crc = 0
	for index in range(2, len(commandBytes)):
		crc += commandBytes[index]
		print 'Byte ', index, ' = ', commandBytes[index]
	crc = 255 - (crc % 256)
	print 'CRC: ', crc
	commandBytes += struct.pack("<B", crc)

	serialPort.write(commandBytes)
	serialPort.flush()
	serialPort.close()

