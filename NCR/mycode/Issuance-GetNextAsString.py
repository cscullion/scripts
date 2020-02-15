import urllib
import xml.etree.ElementTree as ET

params = urllib.urlencode({'GUID': '3212f621-7a75-4cd9-93be-a9d53339e2a8',
    'Criteria': '<SearchCriteria><ExtCRMInterface>DZA-I EPC</ExtCRMInterface></SearchCriteria>'})
f = urllib.urlopen("http://153.73.161.207/connectors/Issuance.asmx/GetNextAsString?%s" % params)
myResponse = f.read()
print myResponse
