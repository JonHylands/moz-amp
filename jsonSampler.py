from sample import *
import json
import signal
import time

def stopJsonSampler(signum, frame):
    raise KeyboardInterrupt, "Signal handler"

def main():
    signal.signal(signal.SIGINT, stopJsonSampler)
    powerLog = []
    serialPortName = "/dev/ttyACM0"
    module = CurrentModule()
    module.startRunning(serialPortName)

    sampleTimeBeforeEpochOffset = time.time()
    sample = module.getSample()
    sampleTimeAfterEpochOffset = time.time()
    sampleTimeEpochOffset = (sampleTimeAfterEpochOffset + sampleTimeBeforeEpochOffset) * 1000.0 / 2.0 - sample.msCounter;
    firstSampleMsCounter = sample.msCounter

    try:
        while True:
            sample = module.getSample()
            current = sample.getCurrent() / 10.0
            sampleObj = {}
            sampleObj['current'] = current;
            sampleObj['time'] = sample.msCounter;
            powerLog.append(sampleObj)
    except KeyboardInterrupt:
        powerProfile = {}
        powerProfile['sampleTimeEpochOffset'] = sampleTimeEpochOffset
        powerProfile['sampleTimeFirst'] = firstSampleMsCounter
        powerProfile['samples'] = powerLog
        print json.dumps(powerProfile, sort_keys=True,
                   indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
