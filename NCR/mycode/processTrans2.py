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
               <item><key>location</key><value>0001</value></item> 
               <item><key>termnum</key><value>00000001</value></item> 
               <item><key>transnum</key><value>00000004</value></item> 
               <item><key>querytype</key><value>4</value></item> 
               <!--                         a-itemtype (0)--> 
               <!--                         | b-itemcode--> 
               <!--                         | |              c-precision (2)--> 
               <!--                         | |              | d-price--> 
               <!--                         | |              | |    e-department--> 
               <!--                         | |              | |    |    f-discountflag--> 
               <!--                         | |              | |    |    | g-minorderflag--> 
               <!--                         | |              | |    |    | | h-itementryid--> 
               <!--                         | |              | |    |    | | |    i-quantity--> 
               <!--                         | |              | |    |    | | |    |         --> 
               <item><key>item1</key><value>0|00004280011300|2|1600|1234|1|0|0010|5|0</value></item> 
               <item><key>item2</key><value>0|00004900001336|2|1500|1234|1|0|0020|3|0</value></item> 
               <item><key>item3</key><value>0|00000250212102|2|1400|1234|1|0|0030|1|0</value></item> 
               <item><key>id</key><value>981000001236</value></item> 
               <item><key>idtype</key><value>0</value></item> 
               <item><key>timestamp</key><value>04/15/15 12:55:22</value></item> 
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
	 webservice = httplib.HTTP("niost.ncrwebhost.com:8080")
	 
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
	 