import struct
import logging
from adafruit_bus_device.i2c_device import I2CDevice
from datetime import timezone, datetime

SET_RTC_CMD = 0
READ_RTC_CMD = 1
READ_WINDSPEED_CMD = 2
READ_WINDDIRECTION_CMD = 3
READ_RAINRATE_CMD = 4
READ_RAINDAILY_CMD = 5


class RainAnemo(object):
    def __init__(self, i2c, addr=0x17):
        self._i2c = i2c
        self.device = I2CDevice(i2c, addr)

    def _rtc_to_dt(self, data):
        year = data[1] + (data[0] << 8)
        month = data[2]
        day = data[3]
        hour = data[5]
        minute = data[6]
        second = data[7]
        dt = datetime(year, month, day, hour=hour,
                      minute=minute, second=second)
        return dt

    def read_rtc(self):
        data = self.read_register(READ_RTC_CMD, 8)
        return self._rtc_to_dt(data)

    def read_wind_speed(self):
        data = self.read_register(READ_WINDSPEED_CMD, 4)
        return self.to_float(data)

    def read_wind_direction(self):
        data = self.read_register(READ_WINDDIRECTION_CMD, 4)
        return self.to_int(data)

    def read_rain_rate(self):
        data = self.read_register(READ_RAINRATE_CMD, 4)
        return self.to_float(data)

    def read_rain_daily(self):
        data = self.read_register(READ_RAINDAILY_CMD, 4)
        return self.to_float(data)

    def set_rtc(self):
        with self.device as device:
            now = datetime.now(timezone.utc)
            year_msb = now.year >> 8
            year_lsb = now.year & 0xff
            dotw = int(datetime.strftime(now, "%w"))
            data = [SET_RTC_CMD, year_msb, year_lsb, now.month, now.day, dotw, now.hour, now.minute,
                    now.second]
            device.write(bytes(data))

    def read_register(self, register: int, length: int) -> bytearray:
        "Read from the device register."
        with self.device as device:
            device.write(bytes([register & 0xFF]))
            result = bytearray(length)
            device.readinto(result)
            return result

    def to_float(self, data: bytearray) -> float:
        byte_string = bytes(data)
        float_value = struct.unpack('f', byte_string)[0]
        return float_value

    def to_int(self, data: bytearray) -> int:
        byte_string = bytes(data)
        int_value = struct.unpack('i', byte_string)[0]
        return int_value


class Davis(object):
    _store = None
    _old_daily_rain = -1
    _old_rain_rate = -1
    _old_wind_speed = -1
    _old_wind_dir = -1

    def __init__(self, i2c, store=None):
        self._device = RainAnemo(i2c)
        self._store = store

        self._device.set_rtc()

        logging.info("Rain gauge ready")

    def read_wind_direction(self):
        value = self._device.read_wind_direction()
        if value != self._old_wind_dir:
            self._store.put_wind_direction("wind_vane", value)
            self._old_wind_dir = value

        logging.debug("Wind direction: %d", value)

    def read_wind_speed(self):
        value = self._device.read_wind_speed()
        if value != self._old_wind_speed:
            self._store.put_wind_speed("anemometer", value)
            self._old_wind_speed = value

        logging.debug("Wind speed: %.2f", value)

    def read_rain_daily(self):
        value = self._device.read_rain_daily()
        if value != self._old_daily_rain:
            self._store.put_daily_rain("daily_rain", value)
            self._old_daily_rain = value

        logging.debug("Daily rain: %.2f ", value)

    def read_rain_rate(self):
        value = self._device.read_rain_rate()
        if value != self._old_rain_rate:
            self._store.put_rain_rate("rain_rate", value)
            self._old_rain_rate = value

        logging.debug("Rain rate: %.2f mm/hr", value)

    def read_rtc(self):
        dt = self._device.read_rtc()
        logging.debug("Davis date: %s", dt)
