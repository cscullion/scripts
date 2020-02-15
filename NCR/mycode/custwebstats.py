#!/usr/bin/python
# custwebstats
#
# This script parses the CustWeb log file and extract interesting timings for certain API calls
#
# rev/author/date/desc
# 1.0  Chris Scullion   20170709   Original
# 1.1  Chris Scullion   20170710   Add optin stats
# 1.2  Chris Scullion   20170711   Clean up output
# 1.3  Chris Scullion   20170712   Include log file name in output
#                                  remove dependency on server name in OfferList END log line
# 1.4  Chris Scullion   20170725   refactoring
# 1.5  Chris Scullion   20170726   added 2-second response time stats
# 1.6  Chris Scullion   20170801   added participating server list
#                                  commented out 2-second response time stats

version = 'custwebstats rev 1.6'

import sys
import datetime
import string

class stats:
    def __init__(self, desc):
        self.description = desc
        self.elapsed = 0.0
        self.count = 0
        self.sum = 0
        self.max = 0.0
        self.min = 9999.9
        self.gt2 = 0
        self.gt5 = 0
        self.gt10 = 0
        self.serverNameDict = {}
        
    def update(self, elapsed, serverName):
        # Check if the serverName is already in the dictionary.  If not, add it and
        # initialize the count to zero
        if len(serverName) > 0:
            try:
                temp = self.serverNameDict[serverName]
            except KeyError:
                self.serverNameDict[serverName] = 0
                
        self.elapsed = elapsed
        if self.elapsed > self.max:
            self.max = self.elapsed
        if self.elapsed < self.min:
            self.min = self.elapsed
        if self.elapsed > 2:
            self.gt2 = self.gt2 + 1
        if self.elapsed > 5:
            self.gt5 = self.gt5 + 1
            if len(serverName) > 0:
                self.serverNameDict[serverName] = self.serverNameDict[serverName] + 1
        if self.elapsed > 10:
            self.gt10 = self.gt10 + 1
        self.count = self.count + 1
        self.sum = self.sum + self.elapsed
    
    def output(self):
        print self.description, 'stats:'
        print '    total count   = {0:7d}'.format(self.count)
        print '    average (sec) = {0:10.2f}'.format(self.sum/self.count)
        print '    max     (sec) = {0:10.2f}'.format(self.max)
        print '    min     (sec) = {0:10.2f}'.format(self.min)
        #print '    > 2 count     = {0:7d}  {1:7.2f}%'.format(self.gt2, float(self.gt2)/self.count*100)
        print '    > 5 count     = {0:7d}  {1:7.2f}%'.format(self.gt5, float(self.gt5)/self.count*100)
        print '    >10 count     = {0:7d}  {1:7.2f}%'.format(self.gt10, float(self.gt10)/self.count*100)
        
    def outputServerNameDict(self):
        print 'Participating servers (WebOfferList >5 count):'
        #serverNameList.sort()
        for serverName in self.serverNameDict:
            print '    {:<15} {:7d}'.format(serverName, self.serverNameDict[serverName])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#main program
#

print version

#process command line arguments
infile = sys.argv[len(sys.argv) - 1]  # last parameter is always the input file

#open the input file
try:
    f = open(infile, 'r')
except IOError:
    print 'can\'t find input file: ', infile
    print 'usage: custwebtats input_file'
    sys.exit()

print 'input file = ', infile

wolStats = stats('WebOfferList')
optStats = stats('optin')

fileDate = ''
linecount = 0

#process the input file line by line
for line in f:
    linecount += 1
    
    # WebOfferList call - pull elapsed time from log message
    j = line.find('OfferList - ')
    n = j + 12
    if j > 0:
        j = line.find('- End elapsed time')
        if j > 0:
            k = line.find('time:')
            if k > 0:
                try:
                    serverName = line[n:j]
                    wolStats.update(float(line[k+6:k+11]), serverName)
                except ValueError:
                    continue
    else:
        # Start of OptIn message - get start time from log timestamp
        j = line.find('Executing OptIn Query')
        if j > 0:
            j = line.find('[')
            k = line.find(' (Type=Debug)]')
            timestamp = line[j+1:k]
            if len(timestamp) > 5:
                try:
                    optinStart = datetime.datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S.%f')
                    if len(fileDate) == 0:    #grab a timestamp for the file date
                        fileDate = timestamp[0:10]
                except ValueError:
                    continue
        else:
            # End of OptIn message - calculate elapsed time from difference between start
            # and end log timestamps
            j = line.find('Completed OptIn Query')
            if j > 0:
                j = line.find('[')
                k = line.find(' (Type=Debug)]')
                timestamp = line[j+1:k]
                if len(timestamp) > 5:
                    try:
                        optinEnd = datetime.datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S.%f')
                        optStats.update((optinEnd - optinStart).total_seconds(), '')
                    except ValueError:
                        continue

print 'file date  = ', fileDate

print
wolStats.output()

print
optStats.output()

print
wolStats.outputServerNameDict()
    
f.close()
