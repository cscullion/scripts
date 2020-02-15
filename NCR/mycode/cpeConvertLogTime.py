import sys
import datetime

for line in sys.stdin:
    j = line.find('[')
    k = line.find(']')
    timestamp = line[j+1:k]
    try:
        dt = datetime.datetime.fromtimestamp(float(timestamp))
        print '{0}{1}{2}'.format(line[:j+1], dt.strftime('%Y-%m-%d %H:%M:%S.%f'), line[k:]),
    except ValueError:
        print line,

