import logging
import adafruit_lps2x
from weather import utils


class Lps22(object):
    _sensor = None
    _temp_cb = None

    def __init__(self, i2c, temp_fun):
        self._sensor = adafruit_lps2x.LPS22(i2c)
        self._temp_cb = temp_fun

        logging.info("LPS22 ready")

    def read(self, elevation=0):
        lps = self._sensor

        logging.debug("Pressure: %.2f hPa", lps.pressure)
        logging.debug("Sea Level Pressure: %.2f hPa",
                      utils.sea_level_pressure(lps.pressure,
                                               temp=self._temp_cb(),
                                               elevation=elevation))
        # print("Temperature: %.2f C" % lps.temperature)

    def pressure(self):
        # this is local pressure, not adjusted to sea level
        return self._sensor.pressure

    def sea_level_pressure(self, elevation=0):
        return utils.sea_level_pressure(self._sensor.pressure, elevation=elevation)
