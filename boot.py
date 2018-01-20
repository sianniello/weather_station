from machine import UART, RTC
import os

uart = UART(0, 115200)
os.dupterm(uart)
