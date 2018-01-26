from machine import I2C, ADC
from mqtt import MQTTClient
import utime
from logging import logging


class SensorNode:
    def __init__(self, io_id, io_user, io_key, frequency, port=1883, battery=False):
        # Turn sensors on/off
        self.sensor_on = True

        # Save variables passed for use in other methods
        self.io_id = io_id
        self.io_user = io_user
        self.io_key = io_key
        self.update_frequency = frequency
        self.port = port
        self.battery = battery

        self.sensor = None

        i2c = I2C(0, I2C.MASTER, pins=('P4', 'P5'))
        utime.sleep_ms(100)
        logging("Weather MQTT client is ready.")

        if battery:
            self.apin = ADC().channel(pin='P13')

    def read_data(self):
        utime.sleep_ms(50)
        value = self.sensor.value if self.sensor else 0
        batt = self.apin() * 0.00176 if self.battery else 0

        return value, batt

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

            client.publish(topic="{0}/feeds/topic".format(self.io_user), msg=str("{0:0.1f}".format(data[0])))

            if self.battery:
                client.publish(topic="{0}/feeds/battery".format(self.io_user),
                               msg=str("{0:0.1f}".format(data[1])))
                print(" >{0} - battery: {1}".format(data[0], data[1]))
            else:
                print(" >{0}".format(data[0]))

        client.check_msg()
