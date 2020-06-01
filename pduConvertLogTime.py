import sys
import datetime

for line in sys.stdin:
    j = 0
    k = line.find('|')
    timestamp = line[j:k]
    try:
        dt = datetime.datetime.fromtimestamp(float(timestamp))
        print('{0}{1}'.format(dt.strftime('%Y-%m-%d %H:%M:%S.%f'), line[k:]), end='')
    except ValueError:
        print('ERROR', timestamp)

