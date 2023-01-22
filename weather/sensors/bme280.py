import board
import logging
from adafruit_bme280 import basic as adafruit_bme280
from weather import utils


class Bme280(object):
    _sensor = None
    _store = None

    def __init__(self, i2c, store=None):
        self._store = store
        self._sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

        logging.info("BME280 ready")

    def read(self, elevation=0):
        bme280 = self._sensor
        temperature = bme280.temperature
        pressure = bme280.pressure
        hum = bme280.relative_humidity
        altitude = bme280.altitude
        sea_pressure = utils.sea_level_pressure(
            pressure, temp=temperature, elevation=elevation)

        self._store.put_temperature("bme280", temperature)
        self._store.put_pressure("bme280", sea_pressure)
        self._store.put_altitude("bme280", altitude)
        self._store.put_humidity("bme280", hum)

        logging.debug("Temperature: %0.1f C" % temperature)
        logging.debug("Humidity: %0.1f %%" % hum)
        logging.debug("Pressure: %0.1f hPa" % pressure)
        logging.debug("Sea Level Pressure: %0.1f hPa" % sea_pressure)
        logging.debug("Altitude = %0.2f meters" % altitude)
