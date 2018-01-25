# main.py -- put your code here!

import utime
import machine
from logging import logging
from weathernode import WeatherNode
from network import WLAN


_IO_ID = "233171"
_IO_USERNAME = "steno87"
_IO_KEY = "2383dd6dc0c74d3aa3d689bbcbf7d63d"
_FREQUENCY = 5  # seconds
_SSID = "NETGEAR55"


def connect():
    wlan = WLAN()
    if not wlan.isconnected():
        wlan.connect(_SSID, auth=(WLAN.WPA2, 'phobiccoconut688'), timeout=5000)
        while not wlan.isconnected():
            machine.idle()

    logging('WLAN connection succeeded!')
    logging("My IP address is: {0}".format(wlan.ifconfig()[0]))


def run():
    weather_mqtt_client = WeatherNode(_IO_ID, _IO_USERNAME, _IO_KEY, _FREQUENCY)
    while True:
        try:
            weather_mqtt_client.run()
        except OSError:
            logging('MQTT connection Error.')
            utime.sleep(60)
            connect()
            continue


run()
