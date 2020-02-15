import sys

list = [
['03', 'MEMBER_ID', [
	['MemberID', 26],
	['CardID', 26],
	['IDStatus', 1],
	['VoidFlag', 1],
	['Type', 2],
	['EntryMode', 1]
]],
['04', 'ITEM_ENTRY',[
    ['itemCode', 16],
    ['itemEntryID', 6],
    ['dept', 4],
    ['deptGroup', 4],
    ['itemFlags', 10],
    ['voidFlag', 1],
    ['unitPrice', 10],
    ['extPrice', 10],
    ['qtytype', 1],
    ['qty', 6],
    ['discountFlag', 1],
    ['minOrderFlag', 1],
	['ManufacturerID', 6],
	['FamilyCode', 3],
	['MixMatchCode', 4],
	['PoolCode', 10],
	['UserItemizerFlag', 1],
    ['description', 18],
	['Total', 10],
	['Subtotal', 10]
]]
]


def parse(id, rs):

	offset = 0

	for msg in list:
		if msg[0] == id:
			print('parsing msg: ', msg[1])
			for field in msg[2]:
				nextoff = offset + field[1]
				print(field[0], ' = ', rs[offset:nextoff])
				offset = nextoff
			break

if __name__ == '__main__':
	print('parsing with protocol 2.81b9')
	if len(sys.argv) < 3:
		print('usage: parse "id" "message text"')
		sys.exit(1)
	inid = sys.argv[1]
	instring = sys.argv[2]
	parse(inid, instring)
