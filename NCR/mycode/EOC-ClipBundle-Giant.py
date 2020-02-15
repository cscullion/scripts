#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime

startTime = datetime.datetime.now()

params = urllib.urlencode({'ExternalSourceID': 'Clippy', 'CustomerOfferData': 'Clippy,Clippy,44123456789\r\nClippy,Clippy,44123456789\r\n'})
#params = urllib.urlencode({'ExternalSourceID': 'TestEOC', 'CustomerOfferData': 'TestEOC,10066,007708227141'})

f = urllib.urlopen("http://153.60.88.132/connectors/ExternalOfferConnector.asmx/ClipBundle?%s" % params)
myResponse = f.read()

print repr(myResponse)

root = ET.fromstring(myResponse)

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime

print '--------------------------------------------------'

print 'elapsed time = ', elapsedTime
