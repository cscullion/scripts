import sys
import thread
import time
import datetime
from ckssimProtocol import protocol_base, protocol_281b9
from ckssimPLU import Item, PLU, Tender, TLU
  
def ScanItem(desc, entryID):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    #                                  ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal
    total, subtotal = p.sendITEM_ENTRY(lItem.upc, entryID, lItem.dept, 0, lItem.price, 1, lItem.desc, total, subtotal)

def ScanItemQty(desc, entryID, qty):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    #                                  ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal
    total, subtotal = p.sendITEM_ENTRY(lItem.upc, entryID, lItem.dept, 0, lItem.price, qty, lItem.desc, total, subtotal)

def ScanItemTrigger(upc, entryID):
    global p
    global total
    global subtotal
    
    #                                         ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal
    total, subtotal = p.sendITEM_ENTRYTrigger(upc, entryID, 0, 0, 0, 1, '', total, subtotal)

def VoidItem(desc, entryID):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    total, subtotal = p.sendITEM_ENTRY(lItem.upc, entryID, lItem.dept, 1, lItem.price, 1, lItem.desc, total, subtotal)

def AdjustItem(desc, amount, entryID, originalEntryID):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    #                                   ItemCode, EntryID, ItemEntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal
    total, subtotal = p.sendADJUSTMENTS(lItem.upc, entryID, originalEntryID, lItem.dept, 0, amount, 1, lItem.desc, total, subtotal)
    
    
def EnterTender(desc, tenderAmt, entryID):
    global p
    global tlu
    
    lTender = tlu.getTender(desc)
    #                  EntryID, TenderID, TenderSubID, BinNum, VoidFlag, TenderAmount, TenderDesc
    p.sendTENDER_ENTRY(entryID, lTender.tenderID, lTender.tenderSubID, lTender.tenderBin, 0, tenderAmt, lTender.desc)

plu = PLU()
# upc, description, price, department
plu.addItem(Item('00000012340111', 'offer111item', 0.68, 1))
plu.addItem(Item('00000000000323', 'offer112item', 4.01, 1))

tlu = TLU()
# description, tenderID, subID, bin
tlu.addTender(Tender('cash', 11, 12, 0))

total = 0.0
subtotal = 0.0

print(datetime.datetime.now())

p = protocol_281b9('153.73.247.228', 1099, 'cpe01', 1, False)

p.sendSTATUS()

###########################################################################################
p.sendBEGIN_TRANSACTION()
#p.sendMEMBER_ID('002503290114', '002503290114')
p.sendMEMBER_ID('0025032900117', '002503290117')
# p.sendALT_ID('4083909353', '4083909353', '11')

time.sleep(1)

ScanItemQty('offer112item', 2, 1)

#total, subtotal = p.sendITEM_ENTRY('00000000000323',
#	EntryID=3,
#	Dept=1,
#	VoidFlag=0,
#	UnitPrice=24.49,
#	Qty=1,
#	Description='offer112item',
#	Total=total,
#	Subtotal=subtotal)

p.sendTOTAL(total, subtotal)

total -= p.getDiscounts()

EnterTender('cash', total, 7)

p.sendEND_OF_SALE(0)

for i in range(1, 5):
    p.flush()
        
p.close()
