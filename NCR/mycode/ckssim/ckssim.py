import sys
import thread
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

tlu = TLU()
# description, tenderID, subID, bin
tlu.addTender(Tender('ckstender', 1, 1, 0))

#p = protocol_281b9('153.73.161.206', 1099, '126', 1, False)
p = protocol_281b9('153.73.240.126', 1099, '126', 1, False)

total = 0.0
subtotal = 0.0

p.sendSTATUS()

###########################################################################################
p.sendBEGIN_TRANSACTION()
#p.sendMEMBER_ID('46100008013', '46100008013')
p.sendMEMBER_ID('446666686650', '446666686650')
#p.sendALT_ID('7706237177', '00000000000', '11')

ScanItem('DeliHam', 1)
ScanItem('Wurst', 2)
ScanItem('OlivLoaf', 3)
ScanItem('DtPepsi', 4)
ScanItem('DtPepsiStap', 5)

AdjustItem('DeliHam', 1.00, 6, 1)

p.sendTOTAL(total, subtotal)

VoidItem('OlivLoaf', 3)

p.sendTOTAL(total, subtotal)

total -= p.getDiscounts()

EnterTender('ckstender', total, 7)

p.sendEND_OF_SALE(0)

for i in range(1, 5):
    p.flush()
        
p.close()
