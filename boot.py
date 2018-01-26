from machine import UART, RTC, idle
import os
from network import WLAN
from logging import logging

uart = UART(0, 115200)
os.dupterm(uart)

_SSID = "NETGEAR55"

wlan = WLAN(mode=WLAN.STA)
wlan.ifconfig(config=('192.168.0.5', '255.255.255.0', '192.168.0.1', '8.8.8.8'))

if not wlan.isconnected():
    wlan.connect(_SSID, auth=(WLAN.WPA2, 'phobiccoconut688'), timeout=5000)
    while not wlan.isconnected():
        idle()  # save power while waiting

logging('WLAN connection succeeded!')
logging("My IP address is: {0}".format(wlan.ifconfig()[0]))

try:
    RTC().ntp_sync("0.it.pool.ntp.org")
    logging("Real Time Clock updated.")
except Exception as e:
    logging("Real Time Clock updating failed. Error: {0}".format(e))
