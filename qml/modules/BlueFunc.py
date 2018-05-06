#!/usr/bin/env python3

import datetime

def ElapsedTime(timestamp):

    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970,1,1)
    print(epoch)
    timestampC = (d - epoch).total_seconds()

    timestamp = int(timestamp)
    
    timeH = datetime.datetime.fromtimestamp(timestamp).strftime('%H')
    timeM = datetime.datetime.fromtimestamp(timestamp).strftime('%M')
    timeHC = datetime.datetime.fromtimestamp(timestampC).strftime('%H')
    timeMC = datetime.datetime.fromtimestamp(timestampC).strftime('%M')

    elapsedH = int(float(timeHC) - float(timeH))
    elapsedM = int(float(timeMC) - float(timeM))

    ergebnis = str(elapsedH) + ":" + str(elapsedM)
    
    return ergebnis