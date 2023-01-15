import adafruit_shtc3
import logging


class Shtc3(object):
    _sensor = None

    def __init__(self, i2c):
        self._sensor = adafruit_shtc3.SHTC3(i2c)

        logging.info("SHTC3 ready")

    def read(self):
        sht = self._sensor
        temperature, relative_humidity = sht.measurements
        logging.debug("Temperature: %0.1f C", temperature)
        logging.debug("Humidity: %0.1f %%", relative_humidity)

    def temperature(self):
        temperature, _ = self._sensor.measurements
        return temperature

    def relative_humidity(self):
        _, relative_humidity = self._sensor.measurements
        return relative_humidity
