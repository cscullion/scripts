version = 'OCAMTLogParse2 rev 0.2'

import sys
import time
import datetime

def parseLineStart(buffer):
    global startTS

    currentTimestampText = buffer[:23]
    startTS = datetime.datetime.strptime(currentTimestampText, "%m/%d/%Y %H:%M:%S.%f")

def parseLineEnd(buffer):
    global startTS
    global currentTS
    global maxDiff
    global totalDiff
    global count
    global elapsedSum

    currentTimestampText = buffer[:23]
    currentTS = datetime.datetime.strptime(currentTimestampText, "%m/%d/%Y %H:%M:%S.%f")
    TSDiff = currentTS - startTS
    TSDiffSeconds = TSDiff.total_seconds()
    if (TSDiffSeconds < 100.0) and (TSDiffSeconds > 0):
        if TSDiffSeconds > maxDiff:
            maxDiff = TSDiffSeconds
        count = count + 1
        totalDiff = totalDiff + TSDiffSeconds
#        print TSDiffSeconds, ',', elapsedSum, ',', currentTimestampText
        elapsedSum = 0.0

def parseLineDebug(buffer):
    global elapsedSum
    
    j = buffer.find('~~ Elapsed time: ')
    if j >= 0:
        j = j + 17
        elapsedText = buffer[j:j+6]
        #print 'elapsedText = ', elapsedText
        elapsedSum = elapsedSum + float(elapsedText)
        
startTS = datetime.datetime.now()
currentTS = datetime.datetime.now()
maxDiff = 0.0
count = 0
totalDiff = 0.0
elapsedSum = 0.0

#print 'total, calc, timestamp'

infile = sys.argv[len(sys.argv) - 1]
try:
    f = open(infile, 'r')
except IOError:
    print 'can\'t find input file: ', infile
    print 'usage: OCAMTLogParse input_file'
    sys.exit()

for line in f:
    i = line.find('is working on file')
    if i >= 0:
        parseLineStart(line)
    else:
        i = line.find('Deleting file')
        if i >= 0:
            parseLineEnd(line)
        else:
            i = line.find('(Type= Debug)')
            if i >= 0:
                parseLineDebug(line)

print version
print infile
print 'max elapsed time: ', maxDiff
print 'average elapsed time: ', totalDiff / count

f.close()
