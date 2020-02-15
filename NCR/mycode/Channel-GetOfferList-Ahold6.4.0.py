#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET

# -------------------------------------------------------------------
# Logon
params = urllib.urlencode({'GUID': 'ffda4eee-dd49-4e8a-8046-34093622781b', \
                           'ExtIdentifier': '0000000000000250329', \
                           'ExtIDType': 0, \
                           'Password':''})
f = urllib.urlopen("http://153.73.161.92/connectors/channels/channel.asmx/Logon?%s" % params)
myResponse = f.read()
print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- Logon ----------------------------------------'
for customer in root.iter('Customer'):
    authtoken = customer.find('AuthToken').text
    print 'authtoken = ', authtoken
print '--------------------------------------------------'

# -------------------------------------------------------------------
# GetOfferList
params = urllib.urlencode({'GUID': 'ffda4eee-dd49-4e8a-8046-34093622781b', \
                           'AuthToken': authtoken, \
                           'PageNum': 1})
f = urllib.urlopen("http://153.73.161.92/connectors/channels/channel.asmx/GetOfferList?%s" % params)
myResponse = f.read()
# print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- GetOfferList ---------------------------------'
for offers in root.iter('Offers'):
    for offer in offers.iter('Offer'):
        offerid = offer.find('OfferID').text
        offeroptedin = offer.find('OfferOptedIn').text
        offeroptable = offer.find('OfferOptable').text
        print 'OfferID = ', offerid, ', OfferOptedIn = ', offeroptedin, ' OfferOptable = ', offeroptable

print '--------------------------------------------------'

# -------------------------------------------------------------------
# Logout
params = urllib.urlencode({'GUID': 'ffda4eee-dd49-4e8a-8046-34093622781b', \
                           'AuthToken': authtoken})
f = urllib.urlopen("http://153.73.161.92/connectors/channels/channel.asmx/Logout?%s" % params)
myResponse = f.read()
# print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- Logout ---------------------------------------'
for response in root.iter('Status'):
    print response.attrib.get('responsecode')
print '--------------------------------------------------'

