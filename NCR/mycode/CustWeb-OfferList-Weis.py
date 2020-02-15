#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime

startTime = datetime.datetime.now()

params = urllib.urlencode({'GUID': 'f7ed75a3-1dac-4951-999e-649e2610a4f8', 'CustomerID': '1', 'CustomerTypeID': 0})
f = urllib.urlopen("http://153.73.161.121/Customer/connectors/CustWeb.asmx/OfferList?%s" % params)
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
