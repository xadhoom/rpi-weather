import logging
from pijuice import PiJuice


class Ups(object):
    ups = None
    _store = None

    def __init__(self, store=None, i2c_addr=0x14):
        self.ups = PiJuice(1, i2c_addr)
        self._store = store

        logging.info("UPS sensor ready")

    def read(self):
        status = self.ups.status
        bat_temp = status.GetBatteryTemperature()
        bat_volt = status.GetBatteryVoltage()
        bat_cur = status.GetBatteryCurrent()
        charge = status.GetChargeLevel()

        store = self._store
        store.put_voltage("ups_battery", bat_volt['data'])
        store.put_current("ups_battery", bat_cur['data'])
        store.put_temperature("ups_battery", bat_temp['data'])
        store.put_charge("ups_battery", charge['data'])

        logging.debug("UPS charge %r", charge)
        logging.debug("UPS battery voltage %r", bat_volt)
        logging.debug("UPS battery temperature %r", bat_temp)
        logging.debug("UPS battery current %r", bat_cur)
