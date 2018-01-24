# main.py -- put your code here!

import utime
import sys
from logging import logging
from weathernode import WeatherNode


_IO_ID = "233171"
_IO_USERNAME = "steno87"
_IO_KEY = "2383dd6dc0c74d3aa3d689bbcbf7d63d"
_FREQUENCY = 5  # seconds


def run():
    while True:
        weather_mqtt_client = WeatherNode(_IO_ID, _IO_USERNAME, _IO_KEY, _FREQUENCY)
        logging('MQTT initialized.')
        try:
            weather_mqtt_client.run()
        except OSError:
            logging('MQTT connection Error.')
            utime.sleep(60)
            sys.exit()


run()






