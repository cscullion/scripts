import socket

def sendSTATUS():
    l_req = '0039'                 # MessageLength (4)
    l_req = l_req + '0002'         # TermID (4)
    l_req = l_req + '000001'       # TransID (6)
    l_req = l_req + '69'           # MessageID (2)
    l_req = l_req + '3'            # Request (1)
    l_req = l_req + '        2213' # LocationCode (12)
    l_req = l_req + '    2.81'     # ProtocolVersion (8)
    l_req = l_req + '   9'         # ProtocolBuild (4)
    l_req = l_req + '\r\n'         # Terminator (2)

    print 'sending |' + repr(l_req) + '|'

    totalSent = s.send(l_req)

    print 'sent ', totalSent

def sendBEGIN_TRANSACTION():
    l_req = '0034'                 # MessageLength (4)
    l_req = l_req + '0002'         # TermID (4)
    l_req = l_req + '000001'       # TransID (6)
    l_req = l_req + '10'           # MessageID (2)
    l_req = l_req + '0'            # ResponseFlag (1)
    l_req = l_req + '0'            # TransactionMode (1)
    l_req = l_req + '0'            # TransactionType (1)
    l_req = l_req + '022916'       # StartDate (6)
    l_req = l_req + '161300'       # StartTime (6)
    l_req = l_req + '0000'         # TerminalGroup (4)
    l_req = l_req + '0'            # FuelFlag (1)
    l_req = l_req + '\r\n'         # Terminator (2)

    print 'sending |' + repr(l_req) + '|'

    totalSent = s.send(l_req)

    print 'sent ', totalSent

#HOST = '153.60.64.46'
HOST = '153.60.89.252'
PORT = 1099
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

sendSTATUS()

data = s.recv(1024)
s.close()
print 'Received', repr(data)
