from machine import UART
import os
import utime
import machine
from network import WLAN
from microWebCli import MicroWebCli
from logging import logging

uart = UART(0, 115200)
os.dupterm(uart)


_SSID = "NETGEAR55"
_TIMEZONE_URL = 'http://api.timezonedb.com/v2/get-time-zone?key=1QNTARL4R9XW&by=zone&zone=Europe/Rome&format=json'


wlan = WLAN(mode=WLAN.STA)   # get current object, without changing the mode
# configuration below MUST match your home router settings!!
wlan.ifconfig(config=('192.168.0.5', '255.255.255.0', '192.168.0.1', '8.8.8.8'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect(_SSID, auth=(WLAN.WPA2, 'phobiccoconut688'), timeout=5000)
    while not wlan.isconnected():
        machine.idle()  # save power while waiting

logging('WLAN connection succeeded!')
logging("My IP address is: {0}".format(wlan.ifconfig()[0]))

try:
    contentBytes = MicroWebCli.JSONRequest(_TIMEZONE_URL)
    tuple_data = contentBytes['timestamp']
    machine.RTC(datetime=utime.localtime(tuple_data))
    logging("Real Time Clock updated.")
except Exception as e:
    logging("No remote time service. {0}".format(e))