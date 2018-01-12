from mqtt import MQTTClient
from hcsr04 import HCSR04
import utime
import machine


class TanksNode:
    def __init__(self, io_id, io_user, io_key, frequency, port=1883):
        # Turn sensors on/off
        self.sensor_on = True

        # Save variables passed for use in other methods
        self.io_id = io_id
        self.io_user = io_user
        self.io_key = io_key
        self.update_frequency = frequency
        self.port = port

        self.sensor = HCSR04()
        utime.sleep_ms(100)
        print("Weather MQTT client is ready.")

    def read_data(self):
        utime.sleep_ms(50)
        cm = self.sensor.distance_cm()
        return cm

    def message_callback(self, topic, msg):
        print("[{0}]: {1}".format(topic, msg))
        self.sensor_on = (msg == b'ON')

    def run(self, wlan):
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
            if self.sensor_on and wlan.isconnected():
                data = self.read_data()
                print(" >", data)
                client.publish(topic="{0}/feeds/tank-1".format(self.io_user), msg=str(data))
                utime.sleep(self.update_frequency)
            elif not wlan.isconnected():
                machine.reset()
            client.check_msg()
            utime.sleep(1)
