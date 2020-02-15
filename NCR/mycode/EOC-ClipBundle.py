#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime

startTime = datetime.datetime.now()

params = urllib.urlencode({'ExternalSourceID': 'TestEOC', 'CustomerOfferData': 'TestEOC,10066,007708227141|TestEOC,10066,000000250329|'})

f = urllib.urlopen("http://153.73.161.207/connectors/ExternalOfferConnector.asmx/ClipBundle?%s" % params)
myResponse = f.read()

print repr(myResponse)

root = ET.fromstring(myResponse)

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime

print '--------------------------------------------------'

print 'elapsed time = ', elapsedTime
