#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime

startTime = datetime.datetime.now()

params = urllib.urlencode({'ExternalSourceID': 'TestEOC', 'CustomerID': '044000008006', 'ClientOfferID': '10039'})

f = urllib.urlopen("http://153.60.64.79/connectors/ExternalOfferConnector.asmx/AddCustomerToOffer?%s" % params)
myResponse = f.read()

print myResponse

root = ET.fromstring(myResponse)

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime

print '--------------------------------------------------'
for offers in root.iter('Offers'):
    offerid = offers.find('OfferID').text
    name = offers.find('Name').text
    print 'OfferID = ', offerid, ', Name = ', name
print 'elapsed time = ', elapsedTime
