from machine import I2C
from mqtt import MQTTClient
from hcsr04 import HCSR04
import bme280
import utime


class WeatherNode:
    def __init__(self, io_id, io_user, io_key, frequency, port=1883):
        # Turn sensors on/off
        self.sensor_on = False

        # Save variables passed for use in other methods
        self.io_id = io_id
        self.io_user = io_user
        self.io_key = io_key
        self.update_frequency = frequency
        self.port = port

        i2c = I2C(0, I2C.MASTER, baudrate=100000)
        self.sensor = bme280.BME280(i2c=i2c)
        utime.sleep_ms(100)
        print("Weather MQTT client is ready.")

    def read_data(self):
        utime.sleep_ms(50)
        temp = self.sensor.read_temperature() / 100.00
        humi = self.sensor.read_humidity() / 1024.00
        pres = self.sensor.read_pressure() / 256.00
        return temp, humi, pres

    def message_callback(self, topic, msg):
        print("[{0}]: {1}".format(topic, msg))
        self.sensor_on = (msg == b'ON')

    def run(self):
        # Setup MQTT client
        client = MQTTClient(client_id=self.io_id,
                            server="io.adafruit.com",
                            user=self.io_user,
                            password=self.io_key,
                            port=self.port)
        client.set_callback(self.message_callback)
        client.connect()
        client.subscribe(topic="{0}/feeds/sensors".format(self.io_user))

        while True:
            if self.sensor_on:
                data = self.read_data()
                print(" >", data)
                client.publish(topic="{0}/feeds/temperature".format(self.io_user), msg=str(data[0]))
                client.publish(topic="{0}/feeds/humidity".format(self.io_user), msg=str(data[1]))
                client.publish(topic="{0}/feeds/pressure".format(self.io_user), msg=str(data[2]))
                utime.sleep(self.update_frequency)

            client.check_msg()
            utime.sleep(1)
