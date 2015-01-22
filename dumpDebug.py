import serial
serialPort = serial.Serial(port='/dev/ttyACM0', baudrate=1000000, timeout=1)
commandBytes = bytearray.fromhex("ff ff 01 02 10 EC")
serialPort.write(commandBytes)
serialPort.flush()
serialPort.close()

