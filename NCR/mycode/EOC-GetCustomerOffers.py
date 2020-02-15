#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime
from xml.sax.saxutils import unescape

startTime = datetime.datetime.now()

params = urllib.urlencode({'ExternalSourceID': 'TestEOC', 'CustomerID': '044000008006', 'IncludeAnyCardholders': 'True'})

f = urllib.urlopen("http://153.60.65.207/connectors/ExternalOfferConnector.asmx/GetCustomerOffers?%s" % params)
myResponse = f.read()

myResponse = unescape(myResponse)
print myResponse

# there must be a better way to do this:
# remove the extra <?xml> header and <string> tag
i = myResponse.find('<?xml')
i = myResponse[i+5:].find('<?xml')
j = myResponse.find('</string>')

root = ET.fromstring(myResponse[i+5:j])

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime

print '--------------------------------------------------'
for offers in root.iter('Offers'):
    for offer in offers.iter('Offer'):
        id = offer.get('id')
        logixId = offer.get('logixId')
        name = offer.get('name')
        print 'id = {:<10} logixId = {:<12} name = {:<30}'.format(id, logixId, name)
print 'elapsed time = ', elapsedTime
