import logging
import board
import busio
import pigpio
from .sensors.bme280 import Bme280
from .sensors.lps22 import Lps22
from .sensors.scd41 import Scd41
from .sensors.sgp30 import Sgp30
from .sensors.shtc3 import Shtc3
from .sensors.pm25 import Pm25
from .sensors.rain_gauge import RainGauge
from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler

# location elevation, should be from config
local_elevation = 152


def start_gpios():
    gpio_intf = pigpio.pi()
    if not gpio_intf.connected:
        logging.warning("Could not init connection to pigpio daemon")
        exit()

    return gpio_intf


def run():
    logfmt = "%(asctime)s %(module)-10s: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=logfmt)

    # init bus
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

    # init scheduler
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 1},
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1
    }
    scheduler = Scheduler()
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.configure(executors=executors, job_defaults=job_defaults)

    # init gpios
    gpio_intf = start_gpios()

    # init sensors
    bme280 = Bme280(i2c)
    pm25 = Pm25(i2c)
    shtc3 = Shtc3(i2c)
    lps22 = Lps22(i2c, shtc3.temperature)
    scd41 = Scd41(i2c, lps22.pressure)
    sgp30 = Sgp30(i2c, shtc3.temperature, lps22.pressure,
                  shtc3.relative_humidity)
    # GPIO 26 is pin 37 on rpi
    rain_gauge = RainGauge(gpio_intf, gpio=26)

    # add jobs
    scheduler.add_job(bme280.read, 'interval', kwargs={
                      'elevation': local_elevation}, seconds=60)
    scheduler.add_job(lps22.read, 'interval', kwargs={'elevation':
                                                      local_elevation},
                      seconds=60)
    scheduler.add_job(scd41.read, 'interval',  seconds=60)
    scheduler.add_job(shtc3.read, 'interval',  seconds=60)
    scheduler.add_job(pm25.read, 'interval',  seconds=60)
    scheduler.add_job(sgp30.read, 'interval',  seconds=1)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
