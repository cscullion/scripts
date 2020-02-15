#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
import datetime

update = '''<PointsAdjust programid="1">
<![CDATA[0000000000000250329,0,5
]]>
</PointsAdjust>
'''

params = urllib.urlencode({'GUID': 'd5330d54-f010-4f9f-be15-ac04e6cda4d5', 'UpdateStr': update})

f = urllib.urlopen("http://153.73.161.92/connectors/PointsUpdate.asmx/AdjustPoints?%s" % params)
myResponse = f.read()

print myResponse

