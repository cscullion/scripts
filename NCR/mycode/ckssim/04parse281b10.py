import sys

rewardTypeText = {'00':'CENTS_OFF', '01': 'PERCENT_OFF', '02':'CENTS_OFF_PER_LB', '03':'SELL_AT_PRICE', '04':'SELL_AT_PRICE_PER_LB', '05':'FREE_ITEM', '36':'CENTS_OFF_PER_VOLUME', '41':'STORED_VALUE', '42':'STORED_VALUE_PER_DOLLAR'}
rewardFlagText = {'00':'earned', '01': 'retracted', '02':'replaced'}

def parseITEM_ENTRY(rs):

    offset = 0

    nextoff = offset + 16
    print 'itemCode = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 6
    print 'itemEntryID =', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 4
    print 'dept =', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 4
    print 'deptGroup =', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 6
    print 'itemFlags=', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'voidFlag = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 10
    print 'unitPrice = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 10
    print 'extPrice = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'qtytype = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 6
    print 'qty = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'discountFlag = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'minOrderFlag = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 18
    print 'description = ', rs[offset:nextoff]

instring = sys.argv[1]

parseITEM_ENTRY(instring)
