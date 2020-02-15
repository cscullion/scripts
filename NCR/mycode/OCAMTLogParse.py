version = 'OCAMTLogParse rev 0.2'

import sys
import time
import datetime

def parseLine(buffer):
    global previousTS
    global currentTS
    global maxDiff
    global totalDiff
    global count
    global outlierCount

    previousTS = currentTS
    currentTimestampText = buffer[:23]
    currentTS = datetime.datetime.strptime(currentTimestampText, "%m/%d/%Y %H:%M:%S.%f")
    TSDiff = currentTS - previousTS
    TSDiffSeconds = TSDiff.total_seconds()
    if (TSDiffSeconds < 100.0) and (TSDiffSeconds > 0):
        if TSDiffSeconds > maxDiff:
            maxDiff = TSDiffSeconds
        count = count + 1
        totalDiff = totalDiff + TSDiffSeconds
    # print TSDiffSeconds
    else:
        if (TSDiffSeconds >= 100.0):
            outlierCount = outlierCount + 1

previousTS = datetime.datetime.now()
currentTS = datetime.datetime.now()
maxDiff = 0.0
count = 0
totalDiff = 0.0
outlierCount = 0

print version

infile = sys.argv[len(sys.argv) - 1]
try:
    f = open(infile, 'r')
except IOError:
    print 'can\'t find input file: ', infile
    print 'usage: OCAMTLogParse input_file'
    sys.exit()

for line in f:
    i = line.find('(Type= Debug)')
    if i < 0:
        parseLine(line)

print 'max elapsed time: ', maxDiff
print 'outlierCount: ', outlierCount
print 'average elapsed time: ', totalDiff / count

f.close()
