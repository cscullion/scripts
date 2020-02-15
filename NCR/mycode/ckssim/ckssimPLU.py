class Item:
    def __init__(self, upc, desc, price, dept):
        self.upc = upc
        self.desc = desc
        self.price = price
        self.dept = dept

class PLU:
    def __init__(self):
        self.pluList = []
      
    def addItem(self, item):
        self.pluList.append(item)
        
    def getItem(self, desc):
        result = Item('0', 'empty', 0.0, 0)
        for i in self.pluList:
            if i.desc == desc:
                result = i
                break
        return result

class Tender:
    def __init__(self, desc, tenderID, tenderSubID, tenderBin):
        self.desc = desc
        self.tenderID = tenderID
        self.tenderSubID = tenderSubID
        self.tenderBin = tenderBin
        
class TLU:
    def __init__(self):
        self.tenderList = []
        
    def addTender(self, tender):
        self.tenderList.append(tender)
        
    def getTender(self, desc):
        result = Tender('empty', 0, 0, 0)
        for t in self.tenderList:
            if t.desc == desc:
                result = t
                break
        return result
