import logging
import pigpio


class RainGauge(object):
    gpio = None
    _intf = None
    _cb = None

    def __init__(self, interface, gpio):
        self.gpio = gpio
        self._intf = interface

        self._intf.set_mode(self.gpio, pigpio.INPUT)
        self._intf.set_pull_up_down(self.gpio, pigpio.PUD_UP)
        self._intf.set_glitch_filter(self.gpio, 100)
        self._cb = self._intf.callback(
            self.gpio, pigpio.FALLING_EDGE, self._pulse)

    def _pulse(self, _gpio, _level, _tick):
        logging.debug("Got a rain gauge tip!")
