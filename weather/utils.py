import math


def sea_level_pressure(p, temp=25, elevation=152):
    var1 = 1 - ((0.0065 * elevation) / (temp + (0.0065 * elevation) + 273.15))
    var1 = pow(var1, -5.257)
    return p * var1


def humidity_to_gm3(temp, pressure, humidity):
    # taken from
    # Guide to Meteorological Instruments and Methods of Observation, WMO 2008
    # https://planetcalc.com/2167/
    # https://planetcalc.com/2161/
    # http://www.michell.com/it/calculator/
    temp_k = temp + 273.15

    # pressure function, used to correct the sat vap pressure
    pressure_fn = 1.0016 + 3.15*pow(10, -6)*pressure - 0.074/pressure

    # saturation vapor pressure in pure phase
    ew = 6.112 * math.exp((17.62 * temp) / (243.12 + temp))

    # saturation vapor pressure of moist air, in hPa
    ew_t = pressure_fn * ew
    ew_t_pa = ew_t * 100  # convert to Pascals

    # actual vapor presssure
    e = ew_t_pa * (humidity / 100)

    # mass to volume ratio, derived from law of perfect gases
    # and using the constant for water vapor of 461.5
    abs_hum = e / (461.5 * temp_k)

    return abs_hum * 1000
