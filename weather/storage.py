import logging
from datetime import datetime
from queue import Queue, Full, Empty


class Store(object):
    _q = None

    def __init__(self):
        self._q = Queue(maxsize=0)  # unbounded, for now

    def put_temperature(self, sensor, value):
        data = {"sensor": sensor, "temperature": value, "ts": self.now_ts()}
        self.put(data)

    def put_humidity(self, sensor, value):
        data = {"sensor": sensor, "humidity": value, "ts": self.now_ts()}
        self.put(data)

    def put_pressure(self, sensor, value):
        data = {"sensor": sensor, "pressure": value, "ts": self.now_ts()}
        self.put(data)

    def put_altitude(self, sensor, value):
        data = {"sensor": sensor, "altitude": value, "ts": self.now_ts()}
        self.put(data)

    def put_voltage(self, sensor, value):
        data = {"sensor": sensor, "voltage": value, "ts": self.now_ts()}
        self.put(data)

    def put_current(self, sensor, value):
        data = {"sensor": sensor, "current": value, "ts": self.now_ts()}
        self.put(data)

    def put_co2(self, sensor, value):
        data = {"sensor": sensor, "co2": value, "ts": self.now_ts()}
        self.put(data)

    def put_eco2(self, sensor, value):
        data = {"sensor": sensor, "eco2": value, "ts": self.now_ts()}
        self.put(data)

    def put_tvoc(self, sensor, value):
        data = {"sensor": sensor, "tvoc": value, "ts": self.now_ts()}
        self.put(data)

    def put_charge(self, sensor, value):
        data = {"sensor": sensor, "charge_level": value, "ts": self.now_ts()}
        self.put(data)

    def put_pm10(self, sensor, value):
        data = {"sensor": sensor, "pm1.0": value, "ts": self.now_ts()}
        self.put(data)

    def put_pm25(self, sensor, value):
        data = {"sensor": sensor, "pm2.5": value, "ts": self.now_ts()}
        self.put(data)

    def put_pm100(self, sensor, value):
        data = {"sensor": sensor, "pm10.0": value, "ts": self.now_ts()}
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
        return datetime.utcnow().timestamp()
