#
#  Check Aux Battery
#
#  used with portable harness, to check aux battery voltage level
#

import serial
serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
commandBytes = bytearray.fromhex("ff ff 01 02 19 E3")
serialPort.write(commandBytes)
serialPort.flush()
serialPort.close()

