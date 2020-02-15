import sys

rewardTypeText = {'00':'CENTS_OFF', '01': 'PERCENT_OFF', '02':'CENTS_OFF_PER_LB', '03':'SELL_AT_PRICE', '04':'SELL_AT_PRICE_PER_LB', '05':'FREE_ITEM', '36':'CENTS_OFF_PER_VOLUME', '41':'STORED_VALUE', '42':'STORED_VALUE_PER_DOLLAR'}
rewardFlagText = {'00':'earned', '01': 'retracted', '02':'replaced'}

def parseSAVINGS(rs):

    offset = 0
    saveRec = rs[offset:]

    while len(saveRec) >= 97:
        
        offset = 0
        nextoff = offset + 16
        itemCode = saveRec[offset:nextoff]
        print 'itemCode= ', itemCode
        
        offset = nextoff
        nextoff = offset + 6
        itemEntryID = saveRec[offset:nextoff]
        print 'itemEntryID=', itemEntryID
        
        offset = nextoff
        nextoff = offset + 6
        rewardID = saveRec[offset:nextoff]
        print 'rewardID=', rewardID
        
        offset = nextoff
        nextoff = offset + 10
        extPrice = saveRec[offset:nextoff]
        print 'extPrice=', extPrice
        
        offset = nextoff
        nextoff = offset + 1
        extPriceFlag = saveRec[offset:nextoff]
        print 'extPriceFlag= ', extPriceFlag
        
        offset = nextoff
        nextoff = offset + 1
        extPriceFlagReason = saveRec[offset:nextoff]
        print 'extPriceFlagReason= ', extPriceFlagReason
        
        offset = nextoff
        nextoff = offset + 2
        rewardFlag = saveRec[offset:nextoff]
        print 'rewardFlag= ', rewardFlag, " ", rewardFlagText[rewardFlag]
        
        offset = nextoff
        nextoff = offset + 2
        rewardType = saveRec[offset:nextoff]
        print 'rewardType=', rewardType, ' ', rewardTypeText[rewardType]
        
        offset = nextoff
        nextoff = offset + 1
        qtyType = saveRec[offset:nextoff]
        print 'qtyType=', qtyType
        
        offset = nextoff
        nextoff = offset + 6
        qty = saveRec[offset:nextoff]
        print 'qty=', qty
        
        offset = nextoff
        nextoff = offset + 3
        volumeLimit = saveRec[offset:nextoff]
        print 'volumeLimit=', volumeLimit
        
        offset = nextoff
        nextoff = offset + 4
        savingsDept = saveRec[offset:nextoff]
        print 'savingsDept=', savingsDept
         
        offset = nextoff
        nextoff = offset + 4
        group = saveRec[offset:nextoff]
        print 'group=', group
        
        offset = nextoff
        nextoff = offset + 6
        itemFlags = saveRec[offset:nextoff]
        print 'itemFlags=', itemFlags
        
        offset = nextoff
        nextoff = offset + 10
        promotionCode = saveRec[offset:nextoff]
        print 'promotionCode=', promotionCode
        
        offset = nextoff
        nextoff = offset + 18
        itemDesc = saveRec[offset:nextoff]
        print 'itemDesc=', itemDesc

        offset = nextoff
        nextoff = offset + 1
        discountType = saveRec[offset:nextoff]
        print 'discountType=', discountType

        offset = nextoff
        saveRec = saveRec[offset:]

        if extPriceFlag == '1':
            discount = -1 * float(extPrice)/1000
        else:
            discount = float(extPrice)/1000
        
        print '  recv SAVINGS: item={:>16s}, entry={:>6s}, offer={:>10s}, disc={:6.2f}, qty={:2d}, type={:s}, flag={:s}, desc={:s}'.format(itemCode, itemEntryID, promotionCode, discount, int(qty)/1000, rewardTypeText[rewardType], rewardFlagText[rewardFlag], itemDesc)

instring = sys.argv[1]

parseSAVINGS(instring)
