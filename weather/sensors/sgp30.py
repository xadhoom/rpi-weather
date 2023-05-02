import adafruit_sgp30
import logging
from datetime import datetime
from weather import utils

# according to datasheet, this sensor must be read
# every second to ensure proper operation of the dynamic baseline
# compensation algorithm

# how often to save a value to the store
SAMPLE_INTV = 120

class Sgp30(object):
    _sensor = None
    _temp_cb = None
    _hum_cb = None
    _press_cb = None
    _store = None
    _last_stored_ts = 0

    def __init__(self, i2c, temp_fun, press_fun, hum_fun, store=None):
        self._sensor = adafruit_sgp30.Adafruit_SGP30(i2c)
        self._temp_cb = temp_fun
        self._hum_cb = hum_fun
        self._press_cb = press_fun
        self._store = store
        self._last_stored_ts = 0

        logging.info("SGP30 ready")

    def read(self):
        sgp30 = self._sensor
        eCO2, TVOC = sgp30.iaq_measure()

        logging.debug("eCO2 = %d ppm \t TVOC = %d ppb", eCO2, TVOC)

        if self._utcnow() >= self._last_stored_ts + SAMPLE_INTV:
            self._last_stored_ts = self._utcnow()
            self._store.put_eco2("sgp30", eCO2)
            self._store.put_tvoc("sgp30", TVOC)
            self._set_iaq_hum()

    def _set_iaq_hum(self):
        hum_gm3 = utils.humidity_to_gm3(self._temp_cb(),
                                        self._press_cb(), self._hum_cb())
        self._sensor.set_iaq_humidity(hum_gm3)

    def _utcnow(self):
        now = datetime.utcnow()
        return now.timestamp()

