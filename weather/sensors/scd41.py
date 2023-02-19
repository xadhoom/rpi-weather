import adafruit_scd4x
import time
import logging


class Scd41(object):
    _sensor = None
    serial = None
    _press_cb = None
    _store = None

    def __init__(self, i2c, press_fun, store=None):
        self._sensor = adafruit_scd4x.SCD4X(i2c)
        self.serial = [hex(i) for i in self._sensor.serial_number]
        self._press_cb = press_fun
        self._store = store
        logging.debug("Serial number: %s", self.serial)

        self._sensor.stop_periodic_measurement()  # if any
        self._sensor.factory_reset()
        self._sensor.start_periodic_measurement()

        logging.info("SCD41 ready")

    def read(self):
        scd4x = self._sensor

        scd4x.set_ambient_pressure(int(self._press_cb()))

        while True:
            if scd4x.data_ready:
                co2 = scd4x.CO2
                temperature = scd4x.temperature
                humidity = scd4x.relative_humidity

                self._store.put_co2("scd41", co2)
                self._store.put_temperature("scd41", temperature)
                self._store.put_humidity("scd41", humidity)

                logging.debug("CO2: %d ppm", co2)
                logging.debug("Temperature: %0.1f *C", temperature)
                logging.debug("Humidity: %0.1f %%", humidity)
                break
            else:
                logging.debug("Waiting for first measurement....")
                time.sleep(1)
