using System;
using CRMConsoleAppCS.CRMWebReference;

namespace CRMConsoleAppCS
{
    class Program
    {
        private static OfferDefinition loadOffer(string oid, string eoid, string path)
        {
            OfferDefinition od = new OfferDefinition();

            od.m_offerID = long.Parse(oid);

            od.m_extOfferID = eoid;

            od.m_offerXML = new EncapsulatedXML();
            od.m_offerXML.m_encoded_xml = "junk";

            try
            {
                od.m_offerXML.m_encoded_xml = System.Net.WebUtility.HtmlEncode(System.IO.File.ReadAllText(path));
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }


            return od;
        }
        static void Main(string[] args)
        {
            string logixAddr = "";
            string externalInterfaceID = "";
            string guid = "";
            string oid = "";
            string eoid = "";
            string path = "";

            for (int i = 0; i < args.Length; i++)
            {
                switch(args[i])
                {
                    case "-u":
                        logixAddr = args[i + 1];
                        break;
                    case "-e":
                        externalInterfaceID = args[i + 1];
                        break;
                    case "-g":
                        guid = args[i + 1];
                        break;
                    case "-i":
                        oid = args[i + 1];
                        break;
                    case "-j":
                        eoid = args[i + 1];
                        break;
                    case "-o":
                        path = args[i + 1];
                        break;
                    default:
                        break;
                }
                //Console.Write(i); Console.Write(": ");  Console.WriteLine(args[i]);
            }

            if (logixAddr.Length <= 0)
            {
                Console.Write("Enter Logix web server address (-u): ");
                logixAddr = Console.ReadLine().Trim();
            }

            CRMConsoleAppCS.CRMWebReference.CRMOfferConnector serviceConnection = new CRMConsoleAppCS.CRMWebReference.CRMOfferConnector();
            serviceConnection.Url = "http://" + logixAddr + "/connectors/CRMOfferConnector.asmx";

            CRMConsoleAppCS.CRMWebReference.ExternalInterfaceID eid = new CRMConsoleAppCS.CRMWebReference.ExternalInterfaceID();

            if (externalInterfaceID.Length <= 0)
            {
                Console.Write("Enter external interface ID (-e): ");
                externalInterfaceID = Console.ReadLine().Trim();
            }

            eid.m_extInterfaceID = int.Parse(externalInterfaceID);

            if (guid.Length <= 0)
            {
                Console.Write("Enter CRM Offer Connector guid (-g): ");
                guid = Console.ReadLine().Trim();
            }

            eid.m_eiguid = new Guid(guid);

            Offers os = new Offers();
            os.m_offers = new OfferDefinition[1];

            if (oid.Length <= 0)
            {
                Console.Write("Enter an offer ID (-i): ");
                oid = Console.ReadLine().Trim();
            }

            if (eoid.Length <= 0)
            {
                Console.Write("Enter the external offer id (-j): ");
                eoid = Console.ReadLine().Trim();
            }

            if (path.Length <= 0)
            {
                Console.Write("XML Offer file path (-o): ");
                path = Console.ReadLine().Trim();
            }

            os.m_offers[0] = loadOffer(oid, eoid, path);

            serviceConnection.postOffersEnhancedResponse(eid, os);

            Console.WriteLine("operation complete");

            Console.Write("usage: CRMConsoleAppCS1");
            Console.Write(" -u ");
            Console.Write(logixAddr);
            Console.Write(" -e ");
            Console.Write(externalInterfaceID);
            Console.Write(" -g ");
            Console.Write(guid);
            Console.Write(" -i ");
            Console.Write(oid);
            Console.Write(" -j ");
            Console.Write(eoid);
            Console.Write(" -o ");
            Console.Write(path);
            Console.WriteLine();
        }
    }
}
