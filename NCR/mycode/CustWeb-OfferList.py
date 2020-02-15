#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime

startTime = datetime.datetime.now()

params = urllib.urlencode({'GUID': '61efada9-3761-43b9-a784-15a4a3d98e3d', 'CustomerID': '044000008005', 'CustomerTypeID': 0})
f = urllib.urlopen("http://153.73.161.207/Customer/connectors/CustWeb.asmx/OfferList?%s" % params)
myResponse = f.read()

root = ET.fromstring(myResponse)

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime

print myResponse

print '--------------------------------------------------'
for offers in root.iter('Offers'):
    offerid = offers.find('OfferID').text
    name = offers.find('Name').text
    print 'OfferID = ', offerid, ', Name = ', name
print 'elapsed time = ', elapsedTime
