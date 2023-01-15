import adafruit_sgp30
import logging
from weather import utils

# according to datasheet, this sensor must be read
# every second to ensure proper operation of the dynamic baseline
# compensation algorithm


class Sgp30(object):
    _sensor = None
    _temp_cb = None
    _hum_cb = None
    _press_cb = None

    def __init__(self, i2c, temp_fun, press_fun, hum_fun):
        self._sensor = adafruit_sgp30.Adafruit_SGP30(i2c)
        self._temp_cb = temp_fun
        self._hum_cb = hum_fun
        self._press_cb = press_fun

        logging.info("SGP30 ready")

    def read(self):
        sgp30 = self._sensor

        hum_gm3 = utils.humidity_to_gm3(self._temp_cb(),
                                        self._press_cb(), self._hum_cb())

        sgp30.set_iaq_humidity(hum_gm3)
        eCO2, TVOC = sgp30.iaq_measure()
        raw = sgp30.raw_measure()
        logging.debug("eCO2 = %d ppm \t TVOC = %d ppb", eCO2, TVOC)
        logging.debug("RAW= %r", raw)
