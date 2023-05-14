import logging
import adafruit_lps2x
from weather import utils


class Lps22(object):
    _sensor = None
    _temp_cb = None
    _store = None

    def __init__(self, i2c, temp_fun, store=None):
        self._sensor = adafruit_lps2x.LPS22(i2c)
        self._temp_cb = temp_fun
        self._store = store

        logging.info("LPS22 ready")

    def read(self, elevation=0):
        logging.debug("--- START LPS22 read ---")
        lps = self._sensor
        temperature = lps.temperature
        pressure = lps.pressure
        sea_pressure = utils.sea_level_pressure(
            pressure, temp=self._temp_cb(), elevation=elevation)

        self._store.put_temperature("lps22", temperature)
        self._store.put_pressure("lps22", sea_pressure)

        logging.debug("Pressure: %.2f hPa", pressure)
        logging.debug("Sea Level Pressure: %.2f hPa", sea_pressure)
        logging.debug("Temperature: %.2f C", temperature)
        logging.debug("--- END LPS22 read ---")

    def pressure(self):
        # this is local pressure, not adjusted to sea level
        return self._sensor.pressure

    def sea_level_pressure(self, elevation=0):
        return utils.sea_level_pressure(self._sensor.pressure, elevation=elevation)
