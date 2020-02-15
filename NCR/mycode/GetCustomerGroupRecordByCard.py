import urllib
import xml.etree.ElementTree as ET

params = urllib.urlencode({'GUID': 'fac85389-100b-48f1-b966-1570bbef5aae',
    'CardId': '00000000000000000019',
    'CardTypeID': 0})
f = urllib.urlopen("http://ams-demo.cloudapp.net/customer/connectors/CustWeb.asmx/GetCustomerGroupRecordByCard?%s" % params)
myResponse = f.read()
print myResponse

root = ET.fromstring(myResponse)

for custid in root.iter('CustomerGroupId'):
    print custid.text
