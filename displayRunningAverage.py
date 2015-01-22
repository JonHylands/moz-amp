#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import serial
import time
import platform
from sample import *

print 'Display Running Average'

if platform.system() == "Linux":
    serialPortName = '/dev/ttyACM0'
else:
    serialPortName = 'COM7'
module = CurrentModule()
module.startRunning(serialPortName)

startTime = int(round(time.time() * 1000))
lastPrintTime = startTime
sampleInterval = 1000
hourFactor = 3600000 / sampleInterval
samples = []
milliampHours = 0
while True:
    sample = module.getSample()
    samples.append(sample)
    currentTime = int(round(time.time() * 1000))
    if (currentTime - lastPrintTime) >= sampleInterval:
        sampleCount = len(samples)
        sampleTime = float(sampleInterval / sampleCount)
        totalCurrent = 0
        totalVoltage = 0
        for sample in samples:
            totalCurrent += (sample.getCurrent() / 10.0) # sample is in tenths of a milliamp
            totalVoltage += (sample.getVoltage() / 1000.0) # sample is in millivolts
        current = totalCurrent / sampleCount
        voltage = totalVoltage / sampleCount
        milliampHours += (current / hourFactor)
        if voltage < 3.2:
            print('\a\aLow Voltage Alert!')
        samples = []
        lastPrintTime = int(round(time.time() * 1000))
        elapsedSeconds = int((lastPrintTime - startTime) / 1000)
        elapsedTime = time.strftime("%H:%M:%S", time.gmtime(elapsedSeconds))
        print '{:4.1f} mA - {:1.2f} V : {:s} ({:3.1f} mAh)'.format(current, voltage, elapsedTime, milliampHours)
