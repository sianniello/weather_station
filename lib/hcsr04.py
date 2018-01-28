import machine, time
from machine import Pin, Timer

__version__ = '0.2.0'
__author__ = 'Roberto Sánchez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

_OUT_OF_RANGE = 23200


class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.

    The timeouts received listening to echo pin are converted to OSError('Out of range')

    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin='P4', echo_pin='P5', echo_timeout_us=500*2*38):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin.
        By default is based in sensor limit range (4m)
        """
        self.chrono = Timer.Chrono()
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.chrono.reset()

        self.trigger.value(0)   # Stabilize the sensor
        time.sleep_us(20)

        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)

        self.trigger.value(0)
        # time.sleep_us(20)

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        self.chrono.reset()
        self._send_pulse_and_wait()

        while self.echo() == 0:
            pass

        self.chrono.start()
        while self.echo() == 1:
            pass

        self.chrono.stop()
        pulse_width = float(self.chrono.read_us())
        cm = pulse_width / 58.0

        if pulse_width > _OUT_OF_RANGE:
            print("Out of range")
        else:
            # print("Distance: {0}cm".format(cm))
            pass

        time.sleep_ms(100)

        return cm

