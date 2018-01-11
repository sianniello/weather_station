from network import WLAN
from weathernode import WeatherNode
import machine

_IO_ID = "233171"
_IO_USERNAME = "steno87"
_IO_KEY = "2383dd6dc0c74d3aa3d689bbcbf7d63d"
_FREQUENCY = 5  # seconds
_SSID = "NETGEAR55"


def connect():
    wlan = WLAN(mode=WLAN.STA)
    while not wlan.isconnected():
        nets = wlan.scan()
        for net in nets:
            if net.ssid == _SSID:
                print("Network found")
                wlan.connect(net.ssid, auth=(net.sec, "phobiccoconut688"), timeout=5000)
                while not wlan.isconnected():
                    machine.idle()
                print("WLAN connection succeeded")
                print("IP address: {0}".format(wlan.ifconfig()[0]))
                return True
        return False


def run():
    connect()

    weather_mqtt_client = WeatherNode(_IO_ID, _IO_USERNAME, _IO_KEY, _FREQUENCY)
    weather_mqtt_client.run()
