#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

params = urllib.urlencode({'GUID': '358180fd-5fca-496d-88b7-c1c4118ec22d', \
                           'ExtInterfaceID': '1000', \
                           'EngineID': '2', \
                           'TransactionDate':'08/14/2017 12:00:00 AM', \
                           'CardID':'044000008005', \
                           'CardTypeID':'0', \
                           'ProductID':'00000000017294', \
                           'ProductTypeID':'1', \
                           'ExtLocationCode':'0001'})
f = urllib.urlopen("http://153.60.64.79/connectors/UniversalOfferConnector.asmx/GetOfferListWithFilters?%s" % params)
myResponse = f.read()
print myResponse
f.close()

root = ET.fromstring(myResponse)

i = root.text.find('?>')
newXML = root.text[:i+2] + '<Offers>' + root.text[i+3:] + '</Offers>'
root2 = ET.fromstring(newXML)

print '--------------------------------------------------'
   
for offer in root2.iter('Offer'):
    header = offer.find('Header')
    print header.find('IncentiveID').text, header.find('IncentiveName').text
