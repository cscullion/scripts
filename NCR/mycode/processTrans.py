# infobel client using Python

import sys, httplib

from xml.sax import make_parser, SAXException
from xml.sax.handler import feature_namespaces
#from ListInfobelRecord import ListInfobelRecord

if __name__ == '__main__':

	 SM_TEMPLATE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ams="http://localhost/yb/amssoap">
	 <soapenv:Header/> 
	 <soapenv:Body> 
         <ams:processTrans> 
           <request> 
               <item><key>location</key><value>mikestore1</value></item> 
               <item><key>termnum</key><value>00000000</value></item> 
               <item><key>transnum</key><value>00000001</value></item> 
               <item><key>querytype</key><value>1</value></item> 
               <!--                         a-itemtype (0)--> 
               <!--                         | b-itemcode--> 
               <!--                         | |          c-precision (2)--> 
               <!--                         | |          | d-price--> 
               <!--                         | |          | |    e-department--> 
               <!--                         | |          | |    |    f-discountflag--> 
               <!--                         | |          | |    |    | g-minorderflag--> 
               <!--                         | |          | |    |    | | h-itementryid--> 
               <!--                         | |          | |    |    | | |    i-quantity--> 
               <!--                         | |          | |    |    | | |    |         --> 
               <item><key>item1</key><value>0|0250212100|2|3000|1234|1|0|0010|1</value></item> 
               <item><key>item2</key><value>0|0250212100|2|1000|1234|1|0|0020|1</value></item> 
               <item><key>item3</key><value>0|0250212100|2|1000|1234|1|0|0030|1</value></item> 
               <item><key>timestamp</key><value>02/23/12 12:55:22</value></item> 
               <item><key>languagecode</key><value>en-US</value></item> 
           </request> 
         </ams:processTrans> 
	 </soapenv:Body> 
         </soapenv:Envelope>"""

	 #SoapMessage = SM_TEMPLATE % ("infobel", "test")
	 SoapMessage = SM_TEMPLATE

         print "SOAP MESSAGE: "
	 print SoapMessage

	 #webservice = httplib.HTTP("hal.kapitol.com")
	 webservice = httplib.HTTP("153.60.64.203:8080")
	 
	 #webservice.putrequest("POST", "/infobelservices/service1.asmx")
	 webservice.putrequest("POST", "/ams")

	 #webservice.putheader("Host", "hal.kapitol.com")
	 webservice.putheader("Host", "153.60.64.203:8080")

	 webservice.putheader("User-Agent", "Python Post")
	 webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
	 webservice.putheader("Content-length", "%d" % len(SoapMessage))

	 #webservice.putheader("SOAPAction", "\"http://www.infobel.com/WebService/Search\"")
	 webservice.putheader("SOAPAction", "")

	 webservice.endheaders()
	 webservice.send(SoapMessage)

	 # get the response

	 statuscode, statusmessage, header = webservice.getreply()
	 print "Response: ", statuscode, statusmessage
	 print "headers: ", header

         #print "file: ", webservice.getfile()
         print "RESPONSE: "
         res = webservice.getfile().read()
         print res
         
         # parse the response
	 
	 #parser = make_parser()
	 #parser.setFeature(feature_namespaces, 0)

	 #myHandler = ListInfobelRecord('NumRecs')

	 #parser.setContentHandler(myHandler)

	 #parser.parse(webservice.getfile())
	 