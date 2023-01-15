import adafruit_scd4x
import time
import logging


class Scd41(object):
    _sensor = None
    serial = None
    _press_cb = None

    def __init__(self, i2c, press_fun):
        self._sensor = adafruit_scd4x.SCD4X(i2c)
        self.serial = [hex(i) for i in self._sensor.serial_number]
        self._press_cb = press_fun
        logging.debug("Serial number: %s", self.serial)
        self._sensor.start_periodic_measurement()

        logging.info("SCD41 ready")

    def read(self):
        scd4x = self._sensor

        scd4x.set_ambient_pressure(int(self._press_cb()))

        while True:
            if scd4x.data_ready:
                logging.debug("CO2: %d ppm", scd4x.CO2)
                logging.debug("Temperature: %0.1f *C", scd4x.temperature)
                logging.debug("Humidity: %0.1f %%", scd4x.relative_humidity)
                break
            else:
                logging.debug("Waiting for first measurement....")
                time.sleep(1)
