import urllib
import xml.etree.ElementTree as ET
import datetime

startTime = datetime.datetime.now()

params = urllib.urlencode({'GUID': '424f16d5-41d0-494a-9234-f0989f7b178e', 'GroupID': '4', 'Name': 'ChrisTestLocGrp', 'Description': 'Chris test location group', 'ExtLocationID': '009977', 'LocationName': 'Delhaize QA store 9977', 'ExtBannerID': '3', 'OperationType': 'augment'})
f = urllib.urlopen("http://153.60.65.207/connectors/LogixGroupManagement.asmx/ProcessLocInLocGroupByLogixID?%s" % params)
myResponse = f.read()

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime

print myResponse

print 'elapsed time = ', elapsedTime
