import utime
import machine
from logging import logging
from weathernode import WeatherNode
from network import WLAN

# Power saving version

_IO_ID = "233171"
_IO_USERNAME = "steno87"
_IO_KEY = "2383dd6dc0c74d3aa3d689bbcbf7d63d"
_FREQUENCY = 1  # minutes
_SSID = "NETGEAR55"


def connect():
    wlan = WLAN()
    if not wlan.isconnected():
        wlan.connect(_SSID, auth=(WLAN.WPA2, 'phobiccoconut688'), timeout=5000)
        while not wlan.isconnected():
            machine.idle()


def run():
    sensor_mqtt_client = WeatherNode(_IO_ID, _IO_USERNAME, _IO_KEY, battery=False)
    while True:
        try:
            sensor_mqtt_client.cycle()

            machine.deepsleep(60000 * _FREQUENCY)
        except OSError:
            logging('MQTT connection Error!')
            utime.sleep(60)
            connect()
            continue


run()
