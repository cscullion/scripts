from datetime import datetime
import socket
import abc
import sys

class protocol_base:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, h, p, locationID, termID, detailOutput):
        self.buffer = 'temp'
        self.response = ''
        self.host = h
        self.port = p
        self.locationID = locationID
        self.termID = termID
        self.detail = detailOutput
        self.accumDiscounts = 0.0
        self.memberIDfromAltID = ''
        d = datetime.now()
        self.transID = (d.hour *10000) + (d.minute * 100) + d.second
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'connecting to host: ', self.host, ' port: ', self.port
        self.s.connect((self.host, self.port))
        self.s.settimeout(1.0)
      
    def flush(self):
        try:
            inchar = self.s.recv(1)
            while inchar != '':
                self.response = self.response + inchar
                if inchar == '\n':
                    self.parseResponse(self.response)
                    self.response = ""
                inchar = self.s.recv(1)
        except IOError:
            pass
        return self.response

    def send(self):
        self.s.send(self.buffer)
        if self.detail:
            print 'Sent: ', repr(self.buffer)
        self.flush()
        
    def close(self):
        self.s.close()
        
    def getDiscounts(self):
        print 'accumulated discounts = ', self.accumDiscounts
        return self.accumDiscounts
        
    @abc.abstractmethod
    def parseResponse(self, rs):
        return
        
class protocol_281b9(protocol_base):
    
    def __init__(self, h, p, locationID, termID, detailOutput):
        print 'using protocol 2.81b9'
        self.rewardTypeText = {'00':'CENTS_OFF', '01': 'PERCENT_OFF', '02':'CENTS_OFF_PER_LB', '03':'SELL_AT_PRICE', '04':'SELL_AT_PRICE_PER_LB', '05':'FREE_ITEM', '36':'CENTS_OFF_PER_VOLUME', '41':'STORED_VALUE', '42':'STORED_VALUE_PER_DOLLAR'}
        self.rewardFlagText = {'00':'earned', '01': 'retracted', '02':'replaced'}
        super(protocol_281b9, self).__init__(h, p, locationID, termID, detailOutput)
        self.protBuild = '9'
        
    def sendSTATUS(self):
        length = 27
        self.transID = self.transID + 1
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '{:02d}'.format(69)     # MessageID (2)
        
        self.buffer = self.buffer + '{:1d}'.format(3)       # Status (1)
        self.buffer = self.buffer + '{:>12s}'.format(self.locationID)
        self.buffer = self.buffer + '{:>8s}'.format('2.81') # ProtocolVersion
        self.buffer = self.buffer + '{:>4s}'.format(self.protBuild)    # ProtocolBuild
        self.buffer = self.buffer + '\r\n'
        print 'sent STATUS'
        self.send()
        
    def sendBEGIN_TRANSACTION(self):
        length = 22
        self.transID = self.transID + 1
        d = datetime.now()
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '10'           # MessageID
        
        self.buffer = self.buffer + '1'            # ResponseFlag (1)
        self.buffer = self.buffer + '0'            # TransactionMode (1)
        self.buffer = self.buffer + '0'            # TransactionType (1)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.month, d.day, d.year-2000)       # StartDate (6)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.hour, d.minute, d.second)        # StartTime (6)
        self.buffer = self.buffer + '0011'         # TerminalGroup (4)
        self.buffer = self.buffer + '0'            # FuelFlag (1)
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent BEGIN_TRANSACTION: term = {:04d}, trans = {:06d}, date={:02d}{:02d}{:02d}, time={:02d}{:02d}{:02d}'.format(self.termID, self.transID, d.month, d.day, d.year-2000, d.hour, d.minute, d.second)
        self.send()
        
    def sendMEMBER_ID(self, MemberID, CardID):
        length = 59
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '03'           # MessageID
        
        self.buffer = self.buffer + '{:>026s}'.format(MemberID)
        self.buffer = self.buffer + '{:>026s}'.format(CardID)
        self.buffer = self.buffer + '0'            # IDStatus
        self.buffer = self.buffer + '0'            # VoidFlag
        self.buffer = self.buffer + '00'           # Type
        self.buffer = self.buffer + '1'            # EntryMode
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent MEMBER_ID: ', MemberID
        self.send()

    def sendALT_ID(self, MemberID, CardID, cardType):
        length = 59
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '03'           # MessageID
        
        self.buffer = self.buffer + '{:>026s}'.format(MemberID)
        self.buffer = self.buffer + '{:>026s}'.format(CardID)
        self.buffer = self.buffer + '0'            # IDStatus
        self.buffer = self.buffer + '0'            # VoidFlag
        self.buffer = self.buffer + cardType       # Type
        self.buffer = self.buffer + '1'            # EntryMode
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent MEMBER_ID: ', MemberID
        self.memberIDfromAltID = ''
        self.send()

    def sendITEM_ENTRY(self, ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal):
        length = 134
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '04'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '0000000000'                                     # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000) * (Qty))  # ExtPrice
        self.buffer = self.buffer + '0'                                              # QtyType
        self.buffer = self.buffer + '{:06d}'.format(Qty*1000)                        # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '000000'                                         # ManufacturerID
        self.buffer = self.buffer + '000'                                            # FamilyCode
        self.buffer = self.buffer + '0000'                                           # MixMatchCode
        self.buffer = self.buffer + '0000000000'                                     # PoolCode
        self.buffer = self.buffer + '0'                                              # UserItemizerFlag
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '{:010d}'.format(int(Total * 1000))              # Total
        self.buffer = self.buffer + '{:010d}'.format(int(Subtotal * 1000))           # Subtotal
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ITEM_ENTRY: {:>016s}, qty={:2d}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, Qty, UnitPrice, UnitPrice*Qty, VoidFlag, EntryID)
        self.send()
        if VoidFlag == 1:
            return Total-(Qty*UnitPrice), Subtotal-(Qty*UnitPrice)
        else:
            return Total+(Qty*UnitPrice), Subtotal+(Qty*UnitPrice)

    def sendITEM_ENTRYWgt(self, ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Wgt, Description, Total, Subtotal):
        length = 134
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '04'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '0000000000'                                     # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000) * (Wgt))  # ExtPrice
        self.buffer = self.buffer + '1'                                              # QtyType
        self.buffer = self.buffer + '{:06d}'.format(Wgt*1000)                         # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '000000'                                         # ManufacturerID
        self.buffer = self.buffer + '000'                                            # FamilyCode
        self.buffer = self.buffer + '0000'                                           # MixMatchCode
        self.buffer = self.buffer + '0000000000'                                     # PoolCode
        self.buffer = self.buffer + '0'                                              # UserItemizerFlag
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '{:010d}'.format(int(Total * 1000))              # Total
        self.buffer = self.buffer + '{:010d}'.format(int(Subtotal * 1000))           # Subtotal
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ITEM_ENTRYWgt: {:>016s}, wgt={:2d}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, Wgt, UnitPrice, UnitPrice*Wgt, VoidFlag, EntryID)
        self.send()
        if VoidFlag == 1:
            return Total-(Wgt*UnitPrice), Subtotal-(Wgt*UnitPrice)
        else:
            return Total+(Wgt*UnitPrice), Subtotal+(Wgt*UnitPrice)

    def sendITEM_ENTRYTrigger(self, ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal):
        length = 134
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '04'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '0000000000'                                     # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000) * (Qty))  # ExtPrice
        self.buffer = self.buffer + '4'                                              # QtyType
        self.buffer = self.buffer + '{:06d}'.format(Qty*1000)                        # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '000000'                                         # ManufacturerID
        self.buffer = self.buffer + '000'                                            # FamilyCode
        self.buffer = self.buffer + '0000'                                           # MixMatchCode
        self.buffer = self.buffer + '0000000000'                                     # PoolCode
        self.buffer = self.buffer + '0'                                              # UserItemizerFlag
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '{:010d}'.format(int(Total * 1000))              # Total
        self.buffer = self.buffer + '{:010d}'.format(int(Subtotal * 1000))           # Subtotal
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ITEM_ENTRYTrigger: {:>016s}, qty={:2d}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, Qty, UnitPrice, UnitPrice*Qty, VoidFlag, EntryID)
        self.send()
        if VoidFlag == 1:
            return Total-(Qty*UnitPrice), Subtotal-(Qty*UnitPrice)
        else:
            return Total+(Qty*UnitPrice), Subtotal+(Qty*UnitPrice)

    def sendADJUSTMENTS(self, ItemCode, EntryID, ItemEntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal):
        length = 138
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '05'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:06d}'.format(ItemEntryID)                     # ItemEntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '0000000000'                                     # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000) * (Qty))  # ExtPrice
        self.buffer = self.buffer + '0'                                              # QtyType
        self.buffer = self.buffer + '{:06d}'.format(Qty*1000)                        # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '0'                                              # RewardCalculation
        self.buffer = self.buffer + '1'                                              # AdjustmentType
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '0000000000'                                     # PromotionCode
        self.buffer = self.buffer + '{:010d}'.format(int(Total * 1000))              # Total
        self.buffer = self.buffer + '{:010d}'.format(int(Subtotal * 1000))           # Subtotal
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ADJUSTMENTS: {:>016s}, qty={:2d}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, Qty, UnitPrice, UnitPrice*Qty, VoidFlag, EntryID)
        self.send()
        #reverse total reporting: assumes that an adjustment is a discount, so a void would add to the transaction total
        if VoidFlag == 0:
            return Total-(Qty*UnitPrice), Subtotal-(Qty*UnitPrice)
        else:
            return Total+(Qty*UnitPrice), Subtotal+(Qty*UnitPrice)
        
    def sendTOTAL(self, Total, UserTotal):
        length = 34
        d = datetime.now()
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '06'           # MessageID
        
        self.buffer = self.buffer + '{:010d}'.format(int(Total * 1000))
        self.buffer = self.buffer + '{:010d}'.format(int(UserTotal * 1000))
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.month, d.day, d.year-2000)       # Date (6)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.hour, d.minute, d.second)        # Time (6)
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent TOTAL: ', Total
        self.send()
        
    def sendEND_OF_SALE(self, Status):
        length = 16
        d = datetime.now()
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '08'           # MessageID
        
        self.buffer = self.buffer + '{:02d}'.format(Status)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.month, d.day, d.year-2000)       # Date (6)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.hour, d.minute, d.second)        # Time (6)
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent END_OF_SALE'
        self.send()
        
    def sendTENDER_ENTRY(self, EntryID, TenderID, TenderSubID, BinNum, VoidFlag, TenderAmount, TenderDesc):
        length = 43
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '12'           # MessageID
        
        self.buffer = self.buffer + '{:06d}'.format(EntryID)
        self.buffer = self.buffer + '{:02d}'.format(TenderID)
        self.buffer = self.buffer + '{:02d}'.format(TenderSubID)
        self.buffer = self.buffer + '{:08d}'.format(BinNum)
        self.buffer = self.buffer + '{:01d}'.format(VoidFlag)
        self.buffer = self.buffer + '{:010d}'.format(int(TenderAmount * 1000))
        self.buffer = self.buffer + '{:>12s}'.format(TenderDesc)
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent TENDER_ENTRY: {:12s}, {:7.2f}, void={:1d}, entry={:06}'.format(TenderDesc, TenderAmount, VoidFlag, EntryID)
        self.send()
        
    def parseResponse(self, rs):
        if self.detail:
            print 'parseResponse: detail - ', repr(rs)
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]
        if messageID == '69':
            self.parseSTATUS(rs)
        elif messageID == '50':
            self.parseBEGIN_TRANSACTION_RESPONSE(rs)
        elif messageID == '51':
            self.parseSAVINGS(rs)
        elif messageID == '52':
            self.parseMEMBER_ID_RESPONSE(rs)
        elif messageID == '55':
            self.parseRECEIPT_MESSAGE(rs)
        elif messageID == '59':
            self.parseTOTAL_DONE(rs)
        elif messageID == '60':
            self.parseEOS_DONE(rs)
        elif messageID == '72':
            self.parsePOLL_STATUS_RESPONSE(rs)
        else:
            print 'parseResponse: length=', length, ' termID=', termID, ' transID=', transID, ' messageID=', messageID, ' message=', rs
        return

    def parseSTATUS(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]

        offset = 17
        nextoff = offset + 12
        locationCode = rs[offset:nextoff]
        
        offset = nextoff
        nextoff = offset + 8
        protocolVersion = rs[offset:nextoff]

        offset = nextoff
        nextoff = offset + 4
        protocolBuild = rs[offset:nextoff]
        
        print '  recv STATUS: Loc=', locationCode, ', protVer=', protocolVersion, ', protBuild=', protocolBuild
        if (protocolVersion != '    2.81') or (protocolBuild != '   9'):
            print "*** WARNING: protocol mismatch: continuing, but don't expect good results! ***"
            
    def parseBEGIN_TRANSACTION_RESPONSE(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]
      
        offset = 16
        nextoff = offset + 1
        statusFlag = rs[offset:nextoff]
        
        print '  recv BEGIN_TRANSACTION_RESPONSE: ',
        if statusFlag == '1':
            print 'OK'
        else:
            print 'Handler unavailable'
  
    def parsePOLL_STATUS_RESPONSE(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]
      
        offset = 16
        nextoff = offset + 1
        statusFlag = rs[offset:nextoff]

        offset = nextoff
        nextoff = offset + 24
        dataField = rs[offset:nextoff]
        
        print '  recv POLL_STATUS_RESPONSE: ',
        if statusFlag == '1':
            print 'Connectivity ',
        elif statusFlag == '8':
            print 'IPL ',
        elif statusFlag == '9':
            print 'Database offline ',
        else:
            print 'unknown status ',
        print dataField
   
    def parseTOTAL_DONE(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]
      
        offset = 16
        nextoff = offset + 1
        statusFlag = rs[offset:nextoff]
        
        print '  recv TOTAL_DONE: ',
        if statusFlag == '0':
            print 'Online',
        elif statusFlag == '1':
            print 'Offline',
        elif statusFlag == '2':
            print 'Phone home retry',
        else:
            print 'unknown status ',
        print
    
    def parseEOS_DONE(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]
             
        print '  recv EOS_DONE'

    def parseSAVINGS(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]

        offset = 16
        saveRec = rs[offset:]
        while len(saveRec) > 277:
      #      print saveRec
            
            offset = 0
            nextoff = offset + 16
            itemCode = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            itemEntryID = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            rewardID = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 10
            extPrice = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            extPriceFlag = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            extPriceFlagReason = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            rewardFlag = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            rewardType = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            qtyType = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            qty = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 3
            volumeLimit = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 4
            savingsDept = saveRec[offset:nextoff]
             
            offset = nextoff
            nextoff = offset + 4
            group = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 10
            itemFlags = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 10
            promotionCode = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 18
            itemDesc = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 38
            promoLine1 = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 38
            promoLine2 = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 38
            promoLine3 = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 38
            promoLine4 = saveRec[offset:nextoff]

            offset = nextoff
            nextoff = offset + 1
            discountType = saveRec[offset:nextoff]

            offset = nextoff
            nextoff = offset + 1
            detailedReward = saveRec[offset:nextoff]

            offset = nextoff
            nextoff = offset + 1
            summaryReward = saveRec[offset:nextoff]
           
            offset = nextoff + 6 + 1 + 10 + 5
            saveRec = saveRec[offset:]
 
            if extPriceFlag == '1':
                discount = -1 * float(extPrice)/1000
            else:
                discount = float(extPrice)/1000
            
            if summaryReward == '1':
                self.accumDiscounts += discount
            
            #print '  recv SAVINGS: item={:>16s}, entry={:>6s}, offer={:>10s}, rewID={:>6s}, disc={:6.2f}, qty={:2d}, type={:s}, flag={:s}, detail={:s}, summary={:s}, desc={:s}'.format(itemCode, itemEntryID, promotionCode, rewardID, discount, int(qty)/1000, self.rewardTypeText[rewardType], self.rewardFlagText[rewardFlag], detailedReward, summaryReward, itemDesc)
            print '  recv SAVINGS: item={:>16s}, entry={:>6s}, offer={:>10s}, disc={:6.2f}, qty={:2d}, type={:s}, flag={:s}, detail={:s}, summary={:s}, desc={:s}'.format(itemCode, itemEntryID, promotionCode, discount, int(qty)/1000, self.rewardTypeText[rewardType], self.rewardFlagText[rewardFlag], detailedReward, summaryReward, itemDesc)

    def parseMEMBER_ID_RESPONSE(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]

        offset = 16
        memRec = rs[offset:]
        while len(memRec) > 101:
      #      print memRec
            
            offset = 0
            nextoff = offset + 26
            memberNum = memRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 26
            verifierID = memRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            verifierIDType = memRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 15
            firstName = memRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 25
            lastName = memRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 3
            memFlag = memRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            cardStatusCode = memRec[offset:nextoff]
            
            offset = nextoff
            memRec = memRec[offset:]

            self.memberIDfromAltID = memberNum

            print '  recv MEMBER_ID_RESPONSE: name={:>15s} {:<25s}, memberNum={:>26s}, status={:>2s}'.format(firstName, lastName, self.memberIDfromAltID, cardStatusCode)
              
    def parseRECEIPT_MESSAGE(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]

        offset = 16
        rcpRec = rs[offset:]
        while len(rcpRec) > 44:
      #      print rcpRec
            
            offset = 0
            nextoff = offset + 3
            messID = rcpRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            attrib = rcpRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            extended = rcpRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 38
            printLine = rcpRec[offset:nextoff]
            
            offset = nextoff
            rcpRec = rcpRec[offset:]

            print '  recv RECEIPT_MESSAGE: printLine={:>38s}'.format(printLine)
            
    def getMemberIDfromAltID(self):
        return self.memberIDfromAltID 

class protocol_281b10(protocol_281b9):
    
    def __init__(self, h, p, locationID, termID, detailOutput):
        print 'using protocol 2.81b10'
        self.rewardTypeText = {'00':'CENTS_OFF', '01': 'PERCENT_OFF', '02':'CENTS_OFF_PER_LB', '03':'SELL_AT_PRICE', '04':'SELL_AT_PRICE_PER_LB', '05':'FREE_ITEM', '36':'CENTS_OFF_PER_VOLUME', '41':'STORED_VALUE', '42':'STORED_VALUE_PER_DOLLAR'}
        self.rewardFlagText = {'00':'earned', '01': 'retracted', '02':'replaced'}
        super(protocol_281b10, self).__init__(h, p, locationID, termID, detailOutput)
        self.protBuild = '10'

    def sendITEM_ENTRY(self, ItemCode, EntryID, Dept, VoidFlag, UnitPrice, QtyType, Qty, Description, Total, Subtotal):
        length = 86
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '04'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '000000'                                         # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000 * Qty))    # ExtPrice
        self.buffer = self.buffer + '{:1d}'.format(QtyType)                          # QtyType
        self.buffer = self.buffer + '{:06d}'.format(int(Qty*1000))                   # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ITEM_ENTRY: {:>016s}, qtytype={:1d}, qty={:7.2f}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, QtyType, Qty, UnitPrice, UnitPrice*Qty, VoidFlag, EntryID)
        self.send()
        if VoidFlag == 1:
            return Total-(Qty*UnitPrice), Subtotal-(Qty*UnitPrice)
        else:
            return Total+(Qty*UnitPrice), Subtotal+(Qty*UnitPrice)

    def sendITEM_ENTRYWgt(self, ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Wgt, Description, Total, Subtotal):
        length = 86
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '04'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '000000'                                         # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000) * (Wgt))  # ExtPrice
        self.buffer = self.buffer + '1'                                              # QtyType
        self.buffer = self.buffer + '{:06d}'.format(Wgt*1000)                         # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ITEM_ENTRYWgt: {:>016s}, wgt={:2d}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, Wgt, UnitPrice, UnitPrice*Wgt, VoidFlag, EntryID)
        self.send()
        if VoidFlag == 1:
            return Total-(Wgt*UnitPrice), Subtotal-(Wgt*UnitPrice)
        else:
            return Total+(Wgt*UnitPrice), Subtotal+(Wgt*UnitPrice)

    def sendITEM_ENTRYTrigger(self, ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal):
        length = 86
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '04'           # MessageID
        
        self.buffer = self.buffer + '{:>016s}'.format(ItemCode)                      # ItemCode
        self.buffer = self.buffer + '{:06d}'.format(EntryID)                         # EntryID
        self.buffer = self.buffer + '{:04d}'.format(Dept)                            # Dept
        self.buffer = self.buffer + '0000'                                           # DeptGroup
        self.buffer = self.buffer + '000000'                                         # ItemFlags
        self.buffer = self.buffer + '{:1d}'.format(VoidFlag)                         # VoidFlag
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000))          # UnitPrice
        self.buffer = self.buffer + '{:010d}'.format(int(UnitPrice * 1000) * (Qty))  # ExtPrice
        self.buffer = self.buffer + '4'                                              # QtyType
        self.buffer = self.buffer + '{:06d}'.format(Qty*1000)                        # Qty
        self.buffer = self.buffer + '1'                                              # DiscountFlag
        self.buffer = self.buffer + '1'                                              # MinOrderFlag
        self.buffer = self.buffer + '{:>18s}'.format(Description[0:18])              # Description
        self.buffer = self.buffer + '\r\n'                                           # Terminator (2)
        print 'sent ITEM_ENTRYTrigger: {:>016s}, qty={:2d}, Uprice={:7.2f}, Eprice={:7.2f}, void={:1d}, entry={:06}'.format(ItemCode, Qty, UnitPrice, UnitPrice*Qty, VoidFlag, EntryID)
        self.send()
        if VoidFlag == 1:
            return Total-(Qty*UnitPrice), Subtotal-(Qty*UnitPrice)
        else:
            return Total+(Qty*UnitPrice), Subtotal+(Qty*UnitPrice)
        
    def sendEND_OF_SALE(self, Status, Total):
        length = 26
        d = datetime.now()
        self.buffer = '{:04d}'.format(length + 12)
        self.buffer = self.buffer + '{:04d}'.format(self.termID)
        self.buffer = self.buffer + '{:06d}'.format(self.transID)
        self.buffer = self.buffer + '08'           # MessageID
        
        self.buffer = self.buffer + '{:02d}'.format(Status)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.month, d.day, d.year-2000)       # Date (6)
        self.buffer = self.buffer + '{:02d}{:02d}{:02d}'.format(d.hour, d.minute, d.second)        # Time (6)
        self.buffer = self.buffer + '{:010d}'.format(int(Total * 1000))                            # Total
        self.buffer = self.buffer + '\r\n'         # Terminator (2)
        print 'sent END_OF_SALE'
        self.send()

    def parseSAVINGS(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]

        offset = 16
        saveRec = rs[offset:]
        while len(saveRec) > 97:
      #      print saveRec
            
            offset = 0
            nextoff = offset + 16
            itemCode = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            itemEntryID = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            rewardID = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 10
            extPrice = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            extPriceFlag = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            extPriceFlagReason = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            rewardFlag = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 2
            rewardType = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 1
            qtyType = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            qty = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 3
            volumeLimit = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 4
            savingsDept = saveRec[offset:nextoff]
             
            offset = nextoff
            nextoff = offset + 4
            group = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 6
            itemFlags = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 10
            promotionCode = saveRec[offset:nextoff]
            
            offset = nextoff
            nextoff = offset + 18
            itemDesc = saveRec[offset:nextoff]

            offset = nextoff
            nextoff = offset + 1
            discountType = saveRec[offset:nextoff]

            offset = nextoff
            saveRec = saveRec[offset:]
 
            if extPriceFlag == '1':
                discount = -1 * float(extPrice)/1000
            else:
                discount = float(extPrice)/1000
            
            self.accumDiscounts += discount
        
            print '  recv SAVINGS: item={:>16s}, entry={:>6s}, offer={:>10s}, disc={:6.2f}, qty={:2d}, type={:s}, flag={:s}, desc={:s}'.format(itemCode, itemEntryID, promotionCode, discount, int(qty)/1000, self.rewardTypeText[rewardType], self.rewardFlagText[rewardFlag], itemDesc)

    def parseSTATUS(self, rs):
        length = rs[0:4]
        termID = rs[4:8]
        transID = rs[8:14]
        messageID = rs[14:16]

        offset = 17
        nextoff = offset + 12
        locationCode = rs[offset:nextoff]
        
        offset = nextoff
        nextoff = offset + 8
        protocolVersion = rs[offset:nextoff]

        offset = nextoff
        nextoff = offset + 4
        protocolBuild = rs[offset:nextoff]
        
        print '  recv STATUS: Loc=', locationCode, ', protVer=', protocolVersion, ', protBuild=', protocolBuild
        if (protocolVersion != '    2.81') or (protocolBuild != '  10'):
            print "*** WARNING: protocol mismatch: continuing, but don't expect good results! ***"
