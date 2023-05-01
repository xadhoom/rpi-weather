import logging
import board
import busio
import RPi.GPIO as GPIO
from .storage import Store
from .mqtt import MQTTSender
from .sensors.bme280 import Bme280
from .sensors.lps22 import Lps22
from .sensors.scd41 import Scd41
from .sensors.sgp30 import Sgp30
from .sensors.shtc3 import Shtc3
from .sensors.pm25 import Pm25
from .sensors.davis import Davis
from .sensors.ups import Ups
from .sensors.system import System
from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler

# location elevation, should be from config
local_elevation = 152

# log level
# possible levels, not in correct prio order
# logging.ERROR
# logging.INFO
# logging.WARNING
# logging.CRITICAL
# logging.DEBUG
log_level = logging.DEBUG


def configure_gpios():
    GPIO.setmode(GPIO.BCM)  # see https://pinout.xyz


def run():
    logfmt = "%(asctime)s %(module)-10s: %(message)s"
    logging.basicConfig(level=log_level, format=logfmt)

    # init bus
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

    # init scheduler
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 1},
        'sender': {'type': 'threadpool', 'max_workers': 1},
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1
    }
    scheduler = Scheduler()
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.configure(executors=executors, job_defaults=job_defaults)

    store = Store()
    sender = MQTTSender(store)

    # init gpios
    configure_gpios()

    # init sensors
    bme280 = Bme280(i2c, store=store)
    # 23 is pin 16, 24 is pin 18 on rpi
    pm25 = Pm25(i2c, store=store, set_pin=23, reset_pin=24)
    shtc3 = Shtc3(i2c, store=store)
    lps22 = Lps22(i2c, shtc3.temperature, store=store)
    scd41 = Scd41(i2c, lps22.pressure, store=store)
    sgp30 = Sgp30(i2c, shtc3.temperature, lps22.pressure,
                  shtc3.relative_humidity, store=store)
    ups = Ups(store=store)
    system = System(store=store)
    davis = Davis(i2c, store=store)

    # add jobs
    scheduler.add_job(bme280.read, 'interval', kwargs={
                      'elevation': local_elevation}, seconds=120)
    scheduler.add_job(lps22.read, 'interval', kwargs={'elevation':
                                                      local_elevation},
                      seconds=120)
    scheduler.add_job(scd41.read, 'interval',  seconds=120)
    scheduler.add_job(shtc3.read, 'interval',  seconds=120)
    scheduler.add_job(pm25.read, 'interval',  seconds=10)
    scheduler.add_job(sgp30.read, 'interval',  seconds=1)
    scheduler.add_job(ups.read, 'interval',  seconds=60)
    scheduler.add_job(system.read, 'interval',  seconds=300)

    scheduler.add_job(davis.read_wind_direction, 'interval',  seconds=1)
    scheduler.add_job(davis.read_wind_speed, 'interval',  seconds=1)
    scheduler.add_job(davis.read_rain_rate, 'interval',  seconds=1)
    scheduler.add_job(davis.read_rain_daily, 'interval',  seconds=1)
    scheduler.add_job(davis.read_rtc, 'interval',  seconds=5)

    scheduler.add_job(sender.send, 'interval', executor="sender", seconds=240)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
