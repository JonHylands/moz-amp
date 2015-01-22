import serial
serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
commandBytes = bytearray.fromhex("ff ff 01 02 17 E5")
serialPort.write(commandBytes)
serialPort.flush()
serialPort.close()

