import urllib
import xml.etree.ElementTree as ET

params = urllib.urlencode({'GUID': 'e51e72b5-40a4-412a-baee-fe8447a0ff89'})
f = urllib.urlopen("http://nglogixst.ncrwebhost.com/connectors/Issuance.asmx/GetNext?%s" % params)
myResponse = f.read()
print myResponse
