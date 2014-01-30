from sample import *
import json

def main():
    powerLog = []
    serialPortName = "/dev/cu.usbmodem1451"
    module = CurrentModule()
    module.startRunning(serialPortName)
    try:
        while True:
            sample = module.getSample()
            current = sample.getCurrent() / 10.0
            sampleObj = {}
            sampleObj['current'] = current;
            sampleObj['time'] = sample.msCounter;
            powerLog.append(sampleObj)
    except KeyboardInterrupt:
        print json.dumps(powerLog, sort_keys=True,
                   indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
