import logging
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

# TODO attach reset and set pins

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


class Pm25(object):
    _sensor = None

    def __init__(self, i2c):
        self._sensor = PM25_I2C(i2c, reset_pin)

        logging.info("PM2.5 ready")

    def read(self):
        pm25 = self._sensor

        try:
            aqdata = pm25.read()
            # logging.debug(aqdata)
        except RuntimeError:
            logging.error("Unable to read from sensor !")
            return

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
