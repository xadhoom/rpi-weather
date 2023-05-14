import logging
from datetime import datetime
from queue import Queue, Full, Empty


class Store(object):
    _q = None

    def __init__(self):
        self._q = Queue(maxsize=0)  # unbounded, for now

    def put_temperature(self, sensor, value):
        data = {"s": sensor, "temp": value, "ts": self.now_ts()}
        self.put(data)

    def put_humidity(self, sensor, value):
        data = {"s": sensor, "hum": value, "ts": self.now_ts()}
        self.put(data)

    def put_pressure(self, sensor, value):
        data = {"s": sensor, "pres": value, "ts": self.now_ts()}
        self.put(data)

    def put_altitude(self, sensor, value):
        data = {"s": sensor, "alt": value, "ts": self.now_ts()}
        self.put(data)

    def put_voltage(self, sensor, value):
        data = {"s": sensor, "volt": value, "ts": self.now_ts()}
        self.put(data)

    def put_current(self, sensor, value):
        data = {"s": sensor, "mAh": value, "ts": self.now_ts()}
        self.put(data)

    def put_wattage(self, sensor, value):
        data = {"s": sensor, "W": value, "ts": self.now_ts()}
        self.put(data)

    def put_co2(self, sensor, value):
        data = {"s": sensor, "co2": value, "ts": self.now_ts()}
        self.put(data)

    def put_eco2(self, sensor, value):
        data = {"s": sensor, "eco2": value, "ts": self.now_ts()}
        self.put(data)

    def put_tvoc(self, sensor, value):
        data = {"s": sensor, "tvoc": value, "ts": self.now_ts()}
        self.put(data)

    def put_charge(self, sensor, value):
        data = {"s": sensor, "bat_level": value, "ts": self.now_ts()}
        self.put(data)

    def put_pm10(self, sensor, value):
        data = {"s": sensor, "pm1.0": value, "ts": self.now_ts()}
        self.put(data)

    def put_pm25(self, sensor, value):
        data = {"s": sensor, "pm2.5": value, "ts": self.now_ts()}
        self.put(data)

    def put_pm100(self, sensor, value):
        data = {"s": sensor, "pm10.0": value, "ts": self.now_ts()}
        self.put(data)

    def put_wind_speed(self, sensor, value):
        data = {"s": sensor, "km/h": value, "ts": self.now_ts()}
        self.put(data)

    def put_wind_direction(self, sensor, value):
        data = {"s": sensor, "degrees": value, "ts": self.now_ts()}
        self.put(data)

    def put_rain_rate(self, sensor, value):
        data = {"s": sensor, "mm/hr": value, "ts": self.now_ts()}
        self.put(data)

    def put_daily_rain(self, sensor, value):
        data = {"s": sensor, "mm": value, "ts": self.now_ts()}
        self.put(data)

    def put_ram_pct(self, sensor, value):
        data = {"s": sensor, "fmem_pct": value, "ts": self.now_ts()}
        self.put(data)

    def put(self, data):
        try:
            self._q.put(data, block=False)
        except Full:
            logging.error("Queue full, dropping %r", data)

    def get(self):
        try:
            return self._q.get(block=False)
        except Empty:
            return "__EMPTY__"

    def now_ts(self):
        return int(datetime.utcnow().timestamp())
