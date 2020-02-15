#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

params = urllib.urlencode({'GUID': 'fabc7b17-3918-4bb8-b6fa-d6685b4430c3', \
                           'ExtInterfaceID': '0', \
                           'EngineID': '2', \
                           'OfferID': '1'})
print params
f = urllib.urlopen("http://153.73.161.9/connectors/UniversalOfferConnector.asmx/GetOfferData?%s" % params)
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
    aux = offer.find('Auxilary')
    productGrp = aux.find('ProductGroup')
    productGroupID = productGrp.find('Header').find('ProductGroupID').text
    print 'Product Group = ', productGroupID

print '--------------------------------------------------'

params = urllib.urlencode({'GUID': 'bcc5196c-fbef-4c1d-8aea-421bca27e026', \
                       'ProductGroupID': productGroupID})
f = urllib.urlopen("http://153.73.161.9/connectors/LogixGroupManagement.asmx/GetProductListByGroupID?%s" % params)
myResponse = f.read()
print myResponse
f.close()

root3 = ET.fromstring(myResponse)

print '--------------------------------------------------'

products = root3.find('Products')
for item in products.iter('Item'):
    print 'ExtProductID = ', item.find('ExtProductID').text
    
print '--------------------------------------------------'
