from machine import UART, RTC, idle, SD
from network import WLAN
from logging import logging

_SSID = "NETGEAR55"

rtc = RTC()

wlan = WLAN(mode=WLAN.STA)
wlan.ifconfig(config=('192.168.0.5', '255.255.255.0', '192.168.0.1', '8.8.8.8'))

if not wlan.isconnected():
    wlan.connect(_SSID, auth=(WLAN.WPA2, 'phobiccoconut688'), timeout=5000)
    while not wlan.isconnected():
        idle()  # save power while waiting

if not rtc.synced():
    try:
        rtc.ntp_sync("0.it.pool.ntp.org")
    except Exception as e:
        logging("RTC updating failed: {0}".format(e))
