#
#  Turn On Logging
#
#  used with portable harness, turn on async mode with logging over hardware serial port
#

import serial
serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
commandBytes = bytearray.fromhex("ff ff 01 02 17 E5")
serialPort.write(commandBytes)
serialPort.flush()
serialPort.close()

