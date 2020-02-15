import urllib
import xml.etree.ElementTree as ET
import time

tStart = time.time()
debug = 0

customerCount = 0
webServiceCount = 0

##################################################
# read the customer group list into memory

customerGroupList = list()
f = open('CustomerGroups.txt', 'r')
for line in f:
    groupID = line.strip()
    customerGroupList.append(groupID)
f.close()
print "customerGroupList: ", customerGroupList
print

##################################################
# open customer id list file

f = open('Customers.txt', 'r')

##################################################
# loop through the file, one customer ID per line

for line in f:
    customerCount = customerCount + 1
    customerID = line.strip()

    for groupID in customerGroupList:
        print customerID, groupID,

        # create parameter list for web service call

        params = urllib.urlencode({'GUID': '893b2ba0-588f-4531-ac0a-a80814f1676e',
            'Mode': 'optin',
            'CustomerGroupID': groupID,
            'CustomerID': customerID,
            'CustomerTypeID': 0})
        #print params,
        #print
  
        if debug == 0:
            # encode and make web service call

            webServiceCount = webServiceCount + 1
            w = urllib.urlopen("http://153.60.16.146/customer/connectors/CustWeb.asmx/MembershipEdit?%s" % params)
            myResponse = w.read()
            #print myResponse

            # parse web service response

            root = ET.fromstring(myResponse)
            for result in root.iter('Description'):
                print result.text

f.close()

tEnd = time.time()
print
print "customerCount:   ", customerCount
print "webServiceCount: ", webServiceCount
print "duration:        ", tEnd - tStart