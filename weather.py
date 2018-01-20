from network import WLAN
from weathernode import WeatherNode
import machine
import utime
from microWebCli import MicroWebCli

_IO_ID = "233171"
_IO_USERNAME = "steno87"
_IO_KEY = "2383dd6dc0c74d3aa3d689bbcbf7d63d"
_FREQUENCY = 5  # seconds
_SSID = "NETGEAR55"


def connect():
    wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT)
    wlan.ifconfig(config=('192.168.0.5', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
    wlan.connect(_SSID, auth=(WLAN.WPA2, 'phobiccoconut688'), timeout=5000)

    if not wlan.isconnected:
        machine.Timer.Alarm(idle_callback, 60)

    while not wlan.isconnected():
        machine.idle()  # save power while waiting

    print('WLAN connection succeeded!')
    print("My IP address is: {0}".format(wlan.ifconfig()[0]))

    url = 'http://api.timezonedb.com/v2/get-time-zone?key=1QNTARL4R9XW&by=zone&zone=Europe/Rome&format=json'
    try:
        contentBytes = MicroWebCli.JSONRequest(url)
        tuple_data = contentBytes['timestamp']
        machine.RTC(datetime=utime.localtime(tuple_data))
    except OSError:
        logging("No remote time service.")


def run():
    while True:
        connect()
        logging('Node initialized.')
        weather_mqtt_client = WeatherNode(_IO_ID, _IO_USERNAME, _IO_KEY, _FREQUENCY)
        try:
            weather_mqtt_client.run()
        except OSError:
            logging('MQTT connection Error.')
            utime.sleep(60)


def idle_callback(alarm):
    alarm.cancel()
    logging('Connection lost, trying to re-connect')
    connect()


def logging(msg):
    print(msg)
    with open('log.txt', 'a') as the_file:
        ts = machine.RTC().now()
        the_file.write(msg + 'Timestamp: {0}\r\n'.format(ts))
        the_file.close()
