# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from powertool.mozilla import MozillaAmmeter
import time
import json



ammeterFields = ('current','voltage','time')
serialPortName = "/dev/ttyACM0"
ammeter = MozillaAmmeter(serialPortName, False)


sampleLog = []
stopTime = time.time() + 25
done = False
total = 0.0
count = 0
while not done:
    sample = ammeter.getSample(ammeterFields)
    if sample is not None:
        sampleObj = {}
        sampleObj['current'] = sample['current'].value
        sampleObj['voltage'] = sample['voltage'].value
        sampleObj['time'] = sample['time'].value
        sampleLog.append(sampleObj)
        total = total + sampleObj['current']
        count = count + 1
        if count % 1000 == 0:
            mean = total / count
            print "Running Average: ", round(mean, 2)
    done = (time.time() > stopTime)

ammeter.close()
mean = 0.0
for sample in sampleLog:
    mean = mean + sample['current']
mean = mean / len(sampleLog)
print "\nAverage current: ", round(mean, 2)
