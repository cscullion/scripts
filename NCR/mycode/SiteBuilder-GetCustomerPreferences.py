#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET

# -------------------------------------------------------------------
# Logon
params = urllib.urlencode({'GUID': '81860360-216f-44d2-badd-ec7e77f1f74e', \
                           'ExtIdentifier': '0000000000000250329', \
                           'ExtIDType': 0, \
                           'Password':''})
f = urllib.urlopen("http://153.73.161.92:81/customer/connectors/SiteBuilder.asmx/Logon?%s" % params)
myResponse = f.read()
print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- Logon ----------------------------------------'
for customer in root.iter('Logon'):
    customerPK = customer.find('CustomerPK').text
    print 'customerPK = ', customerPK
print '--------------------------------------------------'

# -------------------------------------------------------------------
# GetCustomerPreferences
params = urllib.urlencode({'GUID': '81860360-216f-44d2-badd-ec7e77f1f74e', \
                           'CustomerPK': customerPK, \
                           'ExtIdentifier': '0000000000000250329', \
                           'ExtIDType': 0, \
                           'ChannelID': 0, \
                           'IgnorePrefStartEnd': 1})
f = urllib.urlopen("http://153.73.161.92:81/customer/connectors/SiteBuilder.asmx/GetCustomerPreferences?%s" % params)
myResponse = f.read()
#print myResponse
f.close()

root = ET.fromstring(myResponse)

print '--- GetCustomerPreferences ---------------------------------'
for preferences in root.iter('Preferences'):
    for preference in preferences.iter('Preference'):
        prefid = preference.find('ID').text
        prefname = preference.find('Name').text
        prefvalue = preference.find('Value').text
        print 'PrefID = ', prefid, ', PrefName = ', prefname, ', PrefValue = ', prefvalue
    
#for offers in root.iter('Offers'):
#    for offer in offers.iter('Offer'):
#        offerid = offer.find('OfferID').text
#        offeroptedin = offer.find('OfferOptedIn').text
#        offeroptable = offer.find('OfferOptable').text
#        print 'OfferID = ', offerid, ', OfferOptedIn = ', offeroptedin, ' OfferOptable = ', offeroptable
#
print '--------------------------------------------------'
