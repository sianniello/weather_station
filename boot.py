import machine
from network import WLAN

# configure the WLAN subsystem in station mode (the default is AP)
wlan = WLAN(mode=WLAN.STA)
# go for fixed IP settings
wlan.ifconfig(config=('192.168.0.5', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
wlan.scan()     # scan for available networks
wlan.connect(ssid='NETGEAR55', auth=(WLAN.WPA2, 'phobiccoconut688'))
while not wlan.isconnected():
    pass
print(wlan.ifconfig())
# enable wake on WLAN
wlan.irq(trigger=WLAN.ANY_EVENT, wake=machine.SLEEP)
# go to sleep
machine.sleep()
# now, connect to the FTP or the Telnet server and the WiPy will wake-up

