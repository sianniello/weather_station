from machine import I2C, ADC
from mqtt import MQTTClient
from bme280 import BME280
import utime
from logging import logging


class WeatherNode:
    def __init__(self, io_id, io_user, io_key, port=1883, battery=False):
        # Turn sensors on/off
        self.sensor_on = True

        # Save variables passed for use in other methods
        self.io_id = io_id
        self.io_user = io_user
        self.io_key = io_key
        self.port = port
        self.battery = battery

        i2c = I2C(0, I2C.MASTER, pins=('P4', 'P5'))
        self.sensor = BME280(i2c=i2c)
        utime.sleep_ms(100)

        if battery:
            self.apin = ADC().channel(pin='P16')

    def read_data(self):
        utime.sleep_ms(50)
        values = self.sensor.values
        temp = values[0]
        pres = values[1]
        humi = values[2]
        batt = self.apin() * 0.0016174 if self.battery else 0

        return temp, humi, pres, batt

    def message_callback(self, topic, msg):
        print("[{0}]: {1}".format(topic, msg))
        self.sensor_on = (msg == b'ON')

    def cycle(self):
        # Setup MQTT client
        client = MQTTClient(client_id=self.io_id,
                            server="io.adafruit.com",
                            user=self.io_user,
                            password=self.io_key,
                            port=self.port)

        client.set_callback(self.message_callback)
        client.connect()
        client.subscribe(topic="{0}/feeds/sensors".format(self.io_user))

        if self.sensor_on:
            # transitory time
            for i in range(0, 9):
                self.read_data()
                utime.sleep(2)

            data = self.read_data()

            client.publish(topic="{0}/feeds/temperature".format(self.io_user), msg=str("{0:0.1f}".format(data[0])))
            client.publish(topic="{0}/feeds/humidity".format(self.io_user), msg=str("{0:0.1f}".format(data[1])))

            client.publish(topic="{0}/feeds/pressure".format(self.io_user),
                           msg=str("{0:0.1f}".format(data[2] / 100)))

            if self.battery:
                client.publish(topic="{0}/feeds/battery".format(self.io_user),
                               msg=str("{0:0.1f}".format(data[3])))
                print(" >{0} - battery: {1}".format(data[0:3], data[3]))
            else:
                print(" >{0}".format(data[0:3]))

        client.check_msg()
        utime.sleep(2)
