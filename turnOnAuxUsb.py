#
#  Turn On Aux USB
#
#  used with extended ammeter, switches on USB  power & data lines for passthrough
#

import serial
serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
commandBytes = bytearray.fromhex("ff ff 01 02 1B E1")
serialPort.write(commandBytes)
serialPort.flush()
serialPort.close()

