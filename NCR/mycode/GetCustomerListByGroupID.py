import urllib
import xml.etree.ElementTree as ET

params = urllib.urlencode({'GUID': '4425119c-e4f7-4588-96a8-43f3f7437013', 'CustomerGroupID': '746', 'CardTypeID': 0})
f = urllib.urlopen("http://ams-demo.cloudapp.net/connectors/LogixGroupManagement.asmx/GetCustomerListByGroupID?%s" % params)
myResponse = f.read()
print myResponse

root = ET.fromstring(myResponse)

for custid in root.iter('ExtCardID'):
    print custid.text
