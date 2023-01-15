import board
import logging
from adafruit_bme280 import basic as adafruit_bme280
from weather import utils


class Bme280(object):
    _sensor = None

    def __init__(self, i2c):
        self._sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

        logging.info("BME280 ready")

    def read(self, elevation=0):
        bme280 = self._sensor
        temperature = bme280.temperature

        logging.debug("Temperature: %0.1f C" % temperature)
        logging.debug("Humidity: %0.1f %%" % bme280.relative_humidity)
        logging.debug("Pressure: %0.1f hPa" % bme280.pressure)
        logging.debug("Sea Level Pressure: %0.1f hPa" %
                      utils.sea_level_pressure(bme280.pressure,
                                               temp=temperature,
                                               elevation=elevation))
        logging.debug("Altitude = %0.2f meters" % bme280.altitude)
