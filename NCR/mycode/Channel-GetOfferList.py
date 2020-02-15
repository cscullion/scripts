#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET

# -------------------------------------------------------------------
# Logon
params = urllib.urlencode({'GUID': 'e8a12464-0ca2-4f59-978b-cbf8945928b1', \
                           'ExtIdentifier': '044000008005', \
                           'ExtIDType': 0, \
                           'Password':''})
f = urllib.urlopen("http://153.60.65.207/connectors/channels/channel.asmx/Logon?%s" % params)
myResponse = f.read()
# print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- Logon ----------------------------------------'
for customer in root.iter('Customer'):
    authtoken = customer.find('AuthToken').text
    print 'authtoken = ', authtoken
print '--------------------------------------------------'

# -------------------------------------------------------------------
# GetOfferList
params = urllib.urlencode({'GUID': 'e8a12464-0ca2-4f59-978b-cbf8945928b1', \
                           'AuthToken': authtoken, \
                           'PageNum': 1})
f = urllib.urlopen("http://153.60.65.207/connectors/channels/channel.asmx/GetOfferList?%s" % params)
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
params = urllib.urlencode({'GUID': 'e8a12464-0ca2-4f59-978b-cbf8945928b1', \
                           'AuthToken': authtoken})
f = urllib.urlopen("http://153.60.65.207/connectors/channels/channel.asmx/Logout?%s" % params)
myResponse = f.read()
# print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- Logout ---------------------------------------'
for response in root.iter('Status'):
    print response.attrib.get('responsecode')
print '--------------------------------------------------'

