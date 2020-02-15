#!/usr/bin/python
# cpeStats
#
# This script parses the CPE ipLog file and matches POS requests (push lines) with CPE responses (pop lines)
# for certain message types and gathers interesting data
#
# rev/author/date/desc
# 1.0  Chris Scullion   20160630   Original
# 1.1  Chris Scullion   20160701   Adding histogram
# 1.2  Chris Scullion   20160702   Adding transaction count
# 1.3  Chris Scullion   20160703   Adding transaction count histogram
# 1.4  Chris Scullion   20160703   Split item message from item counts
# 1.5  Chris Scullion   20160728   Based on mods by Jeff Dixon, adding terminal and transaction number output for all long messages
#                                  Added two command line parameters, -t and -h, and usage output
#                                  Added shell executable line

version = 'cpeStats rev 1.5'

import sys
import datetime

# This class is used to parse the CPE message header to extract terminal, transaction, and message ID
#
class messageHeader:
    def __init__(self):
        self.TermID = ''
        self.TransID = ''
        self.MessageID = ''
        
    def parse(self, buffer):
        self.TermID = buffer[4:8]
        self.TransID = buffer[8:14]
        self.MessageID = buffer[14:16]

# This class is used to parse the 04 (ITEM_ENTRY) message into individual fields.
# It currently only parses up to the quantity field because we only need the void flag
# and quantity to figure out basket size.
#
class message04:
    def __init__(self):
        self.ItemCode = ''
        self.EntryID = ''
        self.Dept = ''
        self.DeptGroup = ''
        self.ItemFlags = ''
        self.VoidFlag = ''
        self.UnitPrice = ''
        self.ExtPrice = ''
        self.QuantityType = ''
        self.Quantity = ''
        
    def parse(self, buffer):
        offset = 16   # message header plus message ID
        self.ItemCode = buffer[offset:offset+16]
        offset += 16
        self.EntryID = buffer[offset:offset+6]
        offset += 6
        self.Dept = buffer[offset:offset+4]
        offset += 4
        self.DeptGroup = buffer[offset: offset+4]
        offset += 4
        self.ItemFlags = buffer[offset:offset+10]
        offset += 10
        self.VoidFlag = buffer[offset:offset+1]
        offset += 1
        self.UnitPrice = buffer[offset:offset+10]
        offset += 10
        self.ExtPrice = buffer[offset:offset+10]
        offset += 10
        self.QuantityType = buffer[offset:offset+1]
        offset += 1
        self.Quantity = buffer[offset:offset+6]
        offset += 6

# This class is used to pair up messages from the POS with responses from CPE.
# It stores the first part (the "push" message) and then calculates elapsed
# time when the second part (the "pop" message) is supplied.
#        
class commandPair:
    def __init__(self, timestamp, terminal, transaction):
        self.ts = float(timestamp)
        self.day = datetime.datetime.fromtimestamp(self.ts).day
        self.term = terminal
        self.trans = transaction
        
    def match(self, timestamp, terminal, transaction):
        dt = datetime.datetime.fromtimestamp(float(timestamp))
        if (terminal == self.term) and (transaction == self.trans):
            return True
        else:
            return False
        
    def pop(self, timestamp):
        self.elapsed = float(timestamp) - self.ts
        
    def getElapsed(self):
        return self.elapsed

# This class calculates and stores transaction-level information. It collects
# and outputs histogram information for the following information for every
# two-hour interval of the day:
# - number of transactions
# - number of item messages
# - number of items (accounting for quantity extensions and voids)
# - number of item adjustment messages
#
class transactionStats:
    def __init__(self):
        self.totalCount = 0
        self.histogram = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.itemMessageHistogram = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.itemCountHistogram = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.aveHistogram = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.adjHistogram = [0,0,0,0,0,0,0,0,0,0,0,0]
        
    def updateTransHistogram(self, ts):
        dt = datetime.datetime.fromtimestamp(float(ts))
        self.histogram[int(dt.hour / 2)] += 1
        
    def updateItemHistogram(self, ts, void, qty):
        dt = datetime.datetime.fromtimestamp(float(ts))
        index = int(dt.hour / 2)
        self.itemMessageHistogram[index] += 1
        if void == '0':
            self.itemCountHistogram[index] += int(qty)/1000
        else:
            self.itemCountHistogram[index] -= int(qty)/1000
        if self.histogram[index] > 0:
            self.aveHistogram[index] = int(self.itemCountHistogram[index] / self.histogram[index])
        
    def updateAdjustmentHistogram(self, ts):
        dt = datetime.datetime.fromtimestamp(float(ts))
        index = int(dt.hour / 2)
        self.adjHistogram[index] += 1

    def printHistogram(self):
        print 'Transactions ',
        for h in self.histogram:
            if h > 0:
                print '{0:5d}'.format(h),
            else:
                print '     ',
        print
        print 'Items        ',
        for h in self.itemCountHistogram:
            if h > 0:
                print '{0:5d}'.format(h),
            else:
                print '     ',
        print
        print 'Average bskt ',
        for h in self.aveHistogram:
            if h > 0:
                print '{0:5d}'.format(h),
            else:
                print '     ',
        print
        print 'ITEM ENTRY   ',
        for h in self.itemMessageHistogram:
            if h > 0:
                print '{0:5d}'.format(h),
            else:
                print '     ',
        print
        print 'ADJUSTMENTS  ',
        for h in self.adjHistogram:
            if h > 0:
                print '{0:5d}'.format(h),
            else:
                print '     ',
        print

# This class collects information about a specified message type. It collects
# and outputs the number of messages of the specified type that had response
# times greater than 10, 20 and 30 seconds, and also collects and outputs
# this information on a two-hour histogram for the day.
#
class messageStats:
    def __init__(self, desc):
        self.maxTime = 0
        self.min = 1000
        self.maxQueue = 0
        self.gt10 = 0
        self.gt20 = 0
        self.gt30 = 0
        self.weightedCount = 0
        self.totalCount = 0
        self.totalTime = 0
        self.messageDesc = desc
        self.histogram = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.longElapsedList = ''
                
    def update(self, ts, elapsed, queueLen, terminal, transaction):
        if elapsed > 10:
            self.gt10 += 1
            self.longElapsedList = self.longElapsedList + '{0:7.2f}   {1:6s}  {2:6s}\n'.format(elapsed, terminal, transaction)
        if elapsed > 20:
            self.gt20 += 1
        if elapsed > 30:
            self.gt30 += 1
        if elapsed > self.maxTime:
            self.maxTime = elapsed
        if elapsed < self.min:
            self.min = elapsed
        if queueLen > self.maxQueue:
            self.maxQueue = queueLen
            
        self.totalCount += 1   #especially useful with BEGIN TRANSACTION since it serves as a overall transaction counter
        
        if elapsed > 0.05:     #try to ignore spurious short-circuited TOTAL messages and others
            self.weightedCount += 1
            self.totalTime = self.totalTime + elapsed
            
        if elapsed > 10:
            dt = datetime.datetime.fromtimestamp(float(ts))
            self.histogram[int(dt.hour / 2)] += 1

    def getMaxTime(self):
        return self.maxTime
        
    def getMaxQueue(self):
        return self.maxQueue
        
    def getAverageTime(self):
        if self.weightedCount > 0:
            return self.totalTime / self.weightedCount
        else:
            return 0
            
    def printMe(self):
        print ',', self.gt10, ',', self.gt20, ',', self.gt30,
      
    @staticmethod
    def printHeader():
        print 'Message         count    >10     >20     >30    maxTime    aveTime  maxQue'
        print '--------------------------------------------------------------------------'
     
    @staticmethod
    def printHeaderHistogram():
        print
        print 'Message/ToD       0     2     4     6     8    10    12    14    16    18    20    22'
        print '-------------------------------------------------------------------------------------'
    
    def printMeAll(self):
        print '{0:<12}    {1:5d}   {2:4d}    {3:4d}    {4:4d}    {5:7.2f}    {6:7.2f}    {7:4d}'.format( \
        self.messageDesc, self.totalCount, self.gt10, self.gt20, self.gt30, self.maxTime, self.getAverageTime(), self.maxQueue)
        
    def printHistogram(self):
        print '{0:<12} '.format(self.messageDesc),
        for h in self.histogram:
            if h > 0:
                print '{0:5d}'.format(h),
            else:
                print '     ',
        print
                
    def printLongList(self):
        if len(self.longElapsedList) > 0:
            print
            print self.messageDesc
            print 'Elapsed   Term     Trans'
            print '------------------------'
            print self.longElapsedList,

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#main program
#

#process command line arguments
allStats = False
longStats = False
infile = sys.argv[len(sys.argv) - 1]  # last parameter is always the input file
for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-a':
        allStats = True
    elif sys.argv[i] == '-t':
        longStats = True
    elif (sys.argv[i] == '-h') or (sys.argv[i] == '/h') or (sys.argv[i] == '-?') or (sys.argv[i] == '/?'):
        print 'usage: cpeStats [-a] [-t] [-h] input_file'
        sys.exit()

#open the input file
try:
    f = open(infile, 'r')
except IOError:
    print 'can\'t find input file: ', infile
    print 'usage: cpeStats [-a] [-t] [-h] input_file'
    sys.exit()

#initialize our data objects
beginTrans = []
memberID = []
totalKey = []

totalStats = messageStats("TOTAL KEY")
memberIDStats = messageStats("MEMBER ID")
beginTransStats = messageStats("BEGIN TRANS")

transStats = transactionStats()

mh = messageHeader()
m04 = message04()

firstTimestamp = ''
lastTimestamp = ''

store = ''

#process the input file line by line
for line in f:
    j = line.find('[')
    k = line.find(']')
    timestamp = line[j+1:k]
    if (len(timestamp) > 0) and (len(timestamp) < 20):
        if len(firstTimestamp) == 0: firstTimestamp = timestamp
        lastTimestamp = timestamp
    i = line.find('push(')
    if i > 0:                             #handle 'push' lines
        mh.parse(line[i+5:])
        terminal = mh.TermID
        transaction = mh.TransID
        if mh.MessageID == '10':    # BEGIN TRANS
            cp = commandPair(timestamp, terminal, transaction)
            beginTrans.append(cp)
            transStats.updateTransHistogram(timestamp)
        if mh.MessageID == '06':    # TOTAL key pressed
            cp = commandPair(timestamp, terminal, transaction)
            totalKey.append(cp)
        if mh.MessageID == '03':    # Member ID
            cp = commandPair(timestamp, terminal, transaction)
            memberID.append(cp)
        if mh.MessageID == '04':    # Item Entry
            m04.parse(line[i+5:])
            transStats.updateItemHistogram(timestamp, m04.VoidFlag, m04.Quantity)
            if m04.UnitPrice != m04.ExtPrice:
                print 'UnitPrice: ', m04.UnitPrice, ', ExtPrice: ', m04.ExtPrice, ', terminal: ', terminal, ', transaction: ', transaction
        if mh.MessageID == '05':    # Item Adjustment
            transStats.updateAdjustmentHistogram(timestamp)
    else:
        i = line.find('pop(')
        if i > 0:                        #handle 'pop' lines
            mh.parse(line[i+4:])
            terminal = mh.TermID
            transaction = mh.TransID
            if mh.MessageID == '50':  # BEGIN TRANS response
                for elem in beginTrans:
                    if elem.match(timestamp, terminal, transaction):
                        elem.pop(timestamp)
                        elapsed = elem.getElapsed()
                        beginTransStats.update(timestamp, elapsed, len(beginTrans), terminal, transaction)
                        beginTrans.remove(elem)   # discard message pair
            if mh.MessageID == '59':  # TOTAL key response
                for elem in totalKey:
                    if elem.match(timestamp, terminal, transaction):
                        elem.pop(timestamp)
                        elapsed = elem.getElapsed()
                        totalStats.update(timestamp, elapsed, len(totalKey), terminal, transaction)
                        totalKey.remove(elem)   # discard message pair
            if mh.MessageID == '52':  # Member ID response
                for elem in memberID:
                    if elem.match(timestamp, terminal, transaction):
                        elem.pop(timestamp)
                        elapsed = elem.getElapsed()
                        memberIDStats.update(timestamp, elapsed, len(memberID), terminal, transaction)
                        memberID.remove(elem)   # discard message pair
        elif len(store) == 0:
            i = line.find('ostat(')   # handle 'ostat' lines (pull store number)
            if i > 0:
                store = line[i+29:i+35]

#output the standard, short version of basic stats
print store,
beginTransStats.printMe()
memberIDStats.printMe()
totalStats.printMe()
print

if allStats:
    #output more detailed stats
    print
    print '  Store: ', store
    print '   file: ', infile
    try:
        dt = datetime.datetime.fromtimestamp(float(firstTimestamp))
        print '   from: ', dt.strftime('%Y%m%d %H:%M')
    except ValueError:
        print '   from: parse error, firstTimestamp = ', firstTimestamp
    try:
        dt = datetime.datetime.fromtimestamp(float(lastTimestamp))
        print '     to: ', dt.strftime('%Y%m%d %H:%M')
    except ValueError:
        print '     to: parse error, lastTimestamp = ', lastTimestamp
    print 'version: ', version
    print

    messageStats.printHeader()
    beginTransStats.printMeAll()
    memberIDStats.printMeAll()
    totalStats.printMeAll()
    
    messageStats.printHeaderHistogram()
    transStats.printHistogram()
    beginTransStats.printHistogram()
    memberIDStats.printHistogram()
    totalStats.printHistogram()

    if longStats:
        beginTransStats.printLongList()
        memberIDStats.printLongList()
        totalStats.printLongList()


f.close()
