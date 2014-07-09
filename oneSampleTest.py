#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
from sample import *

print 'One Sample Test'

serialPortName = "/dev/ttyACM0"
module = CurrentModule()
module.startRunning(serialPortName)

before = time.time()
sample = module.getSample()
after = time.time()

gap = (after - before) * 1000
print "Gap: ", gap
module.stopRunning()

