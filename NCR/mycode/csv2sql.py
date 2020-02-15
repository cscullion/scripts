import sys

tableName = 'myTable'

if len(sys.argv) < 2:
	print("usage: csv2sql [-t <table name>] input_file.csv")
	sys.exit()
for arg in range(1, len(sys.argv)):
	if sys.argv[arg] == '-t':
		tableName = sys.argv[arg + 1]
infile = sys.argv[len(sys.argv) - 1]

try:
	f = open(infile, 'r')
except IOError:
	print("Can't find unput file: ", infile)
	print("usage: csv2sql [-t <table name>] input_file.csv")
	sys.exit()

header = True
for line in f:
	line = line.strip()
	if len(line) > 0:
		tokens = line.split(",")
		if header:
			columns = ""
			for column in tokens:
				columns = columns + column.strip('"') + ","
			columns = columns.strip(",")
			print("column names = ", columns)
		else:
			print("insert into ", tableName, end='')
			print("(", columns, ") values(", end='')
			values = ''
			for token in tokens:
				values = values + token + ','
			values = values.strip(',')
			print(values, ");")
	header = False
f.close()
