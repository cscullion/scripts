import sys

def parseITEM_ENTRY(rs):

    offset = 0

    nextoff = offset + 26
    print 'MemberID = ', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 26
    print 'CardID =', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'IDStatus =', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'VoidFlag =', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 2
    print 'Type=', rs[offset:nextoff]
    
    offset = nextoff
    nextoff = offset + 1
    print 'EntryMode = ', rs[offset:nextoff]

instring = sys.argv[1]

parseITEM_ENTRY(instring)
