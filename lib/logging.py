import machine


def logging(msg):
    print(msg)
    with open('log.txt', 'a') as the_file:
        ts = machine.RTC().now()
        str_ts = '{:02d}-{:02d}-{:02d} {:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4])
        the_file.write(msg + '\t\t{0}\r\n'.format(str_ts))
        the_file.close()
