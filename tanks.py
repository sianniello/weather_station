from network import WLAN
from tanksnode import TanksNode
import machine

_IO_ID = "233171"
_IO_USERNAME = "steno87"
_IO_KEY = "2383dd6dc0c74d3aa3d689bbcbf7d63d"
_FREQUENCY = 5  # seconds
_SSID = "NETGEAR55"


def connect(wlan):
    nets = wlan.scan()
    for net in nets:
        if net.ssid == _SSID:
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, 'phobiccoconut688'), timeout=5000)
            if not wlan.isconnected():
                machine.Timer.Alarm(idle_callback, 60, periodic=True)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting

            print('WLAN connection succeeded!')
            print("My IP address is: {0}".format(wlan.ifconfig()[0]))
            return True
    return False


def run():
    wlan = WLAN(mode=WLAN.STA)
    connect(wlan)

    weather_mqtt_client = TanksNode(_IO_ID, _IO_USERNAME, _IO_KEY, _FREQUENCY)
    weather_mqtt_client.run(wlan)


def idle_callback(alarm):
    alarm.cancel()
    machine.reset()
