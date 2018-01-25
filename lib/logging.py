import machine
from uos import listdir

fileName = 'log.txt'


def logging(msg):
    print(msg)
    if listdir(fileName):
        with open(fileName, 'a') as the_file:
            ts = machine.RTC().now()
            str_ts = '{:02d}-{:02d}-{:02d} {:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4])
            the_file.write('{0:50}{1}\r\n'.format(msg, str_ts))
            the_file.close()
    else:
        with open(fileName, 'w') as the_file:
            ts = machine.RTC().now()
            str_ts = '{:02d}-{:02d}-{:02d} {:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4])
            the_file.write('{0:50}{1}'.format('LOG MESSAGE', 'TIMESTAMP\r\n\r\n'))
            the_file.write('{0:50}{1}\r\n'.format(msg, str_ts))
            the_file.close()
