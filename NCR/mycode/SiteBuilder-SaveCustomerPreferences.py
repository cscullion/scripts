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
# SaveCustomerPreferences
params = urllib.urlencode({'GUID': '81860360-216f-44d2-badd-ec7e77f1f74e', \
                           'CustomerPK': customerPK, \
                           'ExtIdentifier': '0000000000000250329', \
                           'ExtIDType': 0, \
                           'ChannelID': 3, \
                           'ExtLocationCode': 'CustInquiry', \
                           'PreferenceXML': '<CustomerPreferences status="SUBMITTED"><Preferences><Preference><ID>16</ID><Value>01/01/1971</Value></Preference></Preferences></CustomerPreferences>'})
f = urllib.urlopen("http://153.73.161.92:81/customer/connectors/SiteBuilder.asmx/SaveCustomerPreferences?%s" % params)
myResponse = f.read()
print myResponse
f.close()

