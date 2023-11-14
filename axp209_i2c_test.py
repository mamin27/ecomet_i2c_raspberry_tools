#!/usr/bin/python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.axp209 import axp209
import logging

axp = axp209.AXP209()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='axp209.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
axp._logger = logging.getLogger('ecomet.axp209')
axp._logger.info('Start logging ...')

print("internal_temperature: %.2fC" % axp.internal_temperature)
print("battery_exists: %s" % axp.battery_exists)
print("battery_charging: %s" % ("charging" if axp.battery_charging else "done"))
print("battery_current_direction: %s" % ("charging" if axp.battery_current_direction else "discharging"))
print("battery_voltage: %.1fmV" % axp.battery_voltage)
print("battery_discharge_current: %.1fmA" % axp.battery_discharge_current)
print("battery_charge_current: %.1fmA" % axp.battery_charge_current)
print("battery_gauge: %d%%" % axp.battery_gauge)
axp.vbus_write_current_limit('no limit')
print("VBUS current limit: %s" % axp.vbus_read_current_limit)
axp.close()

