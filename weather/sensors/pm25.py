import logging
import pigpio
from datetime import datetime
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

# Reading interval, in sec
# Please note that datasheet suggests to wait at least 30
# seconds after resuming, to let the fan properly
# circulate the air in the chamber.
READ_INTVL_SEC = 180
# Delay in seconds between resuming from sleep
# and performing the actual read. At least 30 seconds.
SPINUP_DELAY_SEC = 45

# TODO attach reset and set pins

# reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False

# NOTE: we call 'em pins, but really they follows GPIOs numbers, see https://pinout.xyz

IDLE = 0
STARTING = 1


class Pm25(object):
    _store = None
    _sensor = None
    _reset_pin = None
    _set_pin = None
    _gpio_intf = None
    _last_ts = None
    _running = False
    _state = IDLE
    _read_interval_sec = READ_INTVL_SEC-SPINUP_DELAY_SEC
    _spinup_delay_sec = SPINUP_DELAY_SEC

    def __init__(self, i2c, gpio_intf, store=None, reset_pin=None, set_pin=None):
        self._store = store
        self._sensor = PM25_I2C(i2c)
        self._reset_pin = reset_pin
        self._set_pin = set_pin
        self._gpio_intf = gpio_intf

        self.init_pins()
        self.shutdown()

        self._last_ts = self._utcnow()

        logging.info("PM2.5 ready")

    def init_pins(self):
        if self._reset_pin:
            self._gpio_intf.set_mode(self._reset_pin, pigpio.OUTPUT)
            self._gpio_intf.write(self._reset_pin, 1)

        if self._set_pin:
            self._gpio_intf.set_mode(self._set_pin, pigpio.OUTPUT)

    def resume(self):
        logging.debug("Resuming PM25 sensor from sleep")

        if self._set_pin:
            self._gpio_intf.write(self._set_pin, 1)

        self._running = True
        self._state = STARTING

    def shutdown(self):
        logging.debug("Putting PM25 sensor to sleep")

        if self._set_pin:
            self._gpio_intf.write(self._set_pin, 0)

        self._running = False
        self._state = IDLE

    def read(self):
        elapsed = self._utcnow() - self._last_ts
        logging.debug("Elapsed %r in state %s", elapsed, self._state)

        if self._state == IDLE:
            if elapsed >= self._read_interval_sec:
                self.resume()
                self._last_ts = self._utcnow()
        elif self._state == STARTING:
            if elapsed >= self._spinup_delay_sec:
                self._read_impl()
                self.shutdown()
                self._last_ts = self._utcnow()

    def _utcnow(self):
        now = datetime.utcnow()
        return now.timestamp()

    def _read_impl(self):
        pm25 = self._sensor

        try:
            aqdata = pm25.read()
            # logging.debug(aqdata)
        except RuntimeError:
            logging.error("Unable to read from sensor !")
            return

        store = self._store
        store.put_pm10("pmsa003i",  aqdata["pm10 env"])
        store.put_pm25("pmsa003i",  aqdata["pm25 env"])
        store.put_pm100("pmsa003i",  aqdata["pm100 env"])

        logging.debug("Standard PM 1.0: %d\tPM2.5: %d\tPM10: %d",
                      aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]
                      )
        logging.debug("Environmental PM 1.0: %d\tPM2.5: %d\tPM10: %d",
                      aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"]
                      )
        logging.debug("Particles > 0.3um / 0.1L air: %d",
                      aqdata["particles 03um"])
        logging.debug("Particles > 0.5um / 0.1L air: %d",
                      aqdata["particles 05um"])
        logging.debug("Particles > 1.0um / 0.1L air: %d",
                      aqdata["particles 10um"])
        logging.debug("Particles > 2.5um / 0.1L air: %d",
                      aqdata["particles 25um"])
        logging.debug("Particles > 5.0um / 0.1L air: %d",
                      aqdata["particles 50um"])
        logging.debug("Particles > 10 um / 0.1L air: %d",
                      aqdata["particles 100um"])
