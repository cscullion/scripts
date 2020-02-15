import sys
import thread
import time
import datetime
from ckssimProtocol import protocol_base, protocol_281b10
from ckssimPLU import Item, PLU, Tender, TLU
  
def ScanItem(desc, entryID):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    #                                  ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal
    total, subtotal = p.sendITEM_ENTRY(lItem.upc, entryID, lItem.dept, 0, lItem.price, 1, lItem.desc, total, subtotal)

def ScanItemQty(desc, entryID, qtyType, qty):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    #                                  ItemCode, EntryID, Dept, VoidFlag, UnitPrice, QtyType, Qty, Description, Total, Subtotal
    total, subtotal = p.sendITEM_ENTRY(lItem.upc, entryID, lItem.dept, 0, lItem.price, qtyType, qty, lItem.desc, total, subtotal)

def ScanItemWgt(desc, entryID, wgt):
    global p
    global plu
    global total
    global subtotal
    
    lItem = plu.getItem(desc)
    #                                  ItemCode, EntryID, Dept, VoidFlag, UnitPrice, Qty, Description, Total, Subtotal
    total, subtotal = p.sendITEM_ENTRYWgt(lItem.upc, entryID, lItem.dept, 0, lItem.price, wgt, lItem.desc, total, subtotal)

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
plu.addItem(Item('0000000333333444', 'DeliHam', 3.49, 3000))
plu.addItem(Item('0000000333333445', 'Wurst', 5.49, 3000))
plu.addItem(Item('0000000333333446', 'OlivLoaf', 4.49, 3000))
plu.addItem(Item('000000120000013', 'DtPepsi', 1.79, 1000))
plu.addItem(Item('13803001198', 'DtPepsiStap', 3.99, 1000))
plu.addItem(Item('1899698432', 'battery pack', 7.99, 1))
plu.addItem(Item('1899698433', 'battery pack A', 5.99, 1))
plu.addItem(Item('00001600027528', 'Shaun basket level item', 5.99, 1))
plu.addItem(Item('00088949727215', 'Plano offer13 item', 5.99, 1))
plu.addItem(Item('00000000004048', 'Limes', 0.86, 1))
plu.addItem(Item('00005100006992', 'Smart WIC', 3.29, 1))
plu.addItem(Item('7160000357', 'Offer 17 item', 3.29, 1))
plu.addItem(Item('4030', 'Offer 18 item', 3.29, 1))
plu.addItem(Item('00000000055991', 'item 55991', 1.00, 1))
plu.addItem(Item('00000000050555', 'item 50555', 1.00, 1))
plu.addItem(Item('00000000060123', 'item 60123', 1.00, 1))
plu.addItem(Item('00002880016205', 'item 2880016205', 5.00, 1))
plu.addItem(Item('00004676800001', 'PDXRxItem', 0.50, 1))
plu.addItem(Item('00000000079101', 'PDXRxItem2', 0.50, 1))
plu.addItem(Item('00000000000300', 'item 300', 1.00, 1))
plu.addItem(Item('00000000000301', 'item 301', 2.00, 1))
plu.addItem(Item('00000000000302', 'item 302', 3.00, 1))
plu.addItem(Item('00000000000303', 'item 303', 4.00, 1))
plu.addItem(Item('00220075044178', 'turkey'  , 1.99, 1))
plu.addItem(Item('00000000000401', 'item 401', 4.00, 1))
plu.addItem(Item('00000000998230', 'fuel', 2.49, 1))
plu.addItem(Item('00000000998330', 'expensive fuel', 4.19, 1))

tlu = TLU()
# description, tenderID, subID, bin
tlu.addTender(Tender('cash', 11, 12, 0))

total = 0.0
subtotal = 0.0

print(datetime.datetime.now())

p = protocol_281b10('localhost', 51098, 'cpe07', 701, False)

p.sendSTATUS()

###########################################################################################

# AUTH transaction

p.sendBEGIN_TRANSACTION()
p.sendMEMBER_ID('000000250329', '000000250329')
time.sleep(1)
ScanItemQty('expensive fuel', 1, 2, 1.00)
p.sendEND_OF_SALE(8, total)
time.sleep(1)

# CAPTURE transaction

p.sendBEGIN_TRANSACTION()
p.sendMEMBER_ID('000000250329', '000000250329')

time.sleep(1)

ScanItemQty('fuel', 1, 2, 3.00)

time.sleep(10)

p.sendTOTAL(total, subtotal)

time.sleep(5)

p.sendTOTAL(total, subtotal)

total -= p.getDiscounts()

EnterTender('cash', total, 7)

p.sendEND_OF_SALE(0, total)

for i in range(1, 5):
    p.flush()
        
p.close()
