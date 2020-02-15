import sys

if len(sys.argv) > 1:
	infile = sys.argv[1]
else:
	infile = 'ipLog'
	
f = open(infile, 'r')
print 'dir, time, terminal, transaction'
for line in f:
	j = line.find('[')
	k = line.find(']')
	timestamp = line[j+1:k]
	i = line.find('push(')
	if i > 0:
		if line[i+19:i+21] == '06':    # TOTAL key pressed
			terminal = line[i+9:i+13]
			transaction = line[i+13:i+19]
			print 'push,', timestamp, ',', terminal, ',', transaction
	else:
		i = line.find('pop(')
		if i > 0:
			if line[i+18:i+20] == '59':  # TOTAL key response
				terminal = line[i+8:i+12]
				transaction = line[i+12:i+18]
				print 'pop, ', timestamp, ',', terminal, ',', transaction
