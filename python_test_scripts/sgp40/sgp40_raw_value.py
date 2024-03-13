#!/usr/bin/python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.sgp40 import sgp40
from  ecomet_i2c_sensors.hdc1080 import hdc1080
import logging
from time import sleep

#set IICbus elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
sgp40=sgp40.SGP40()
sens = hdc1080.HDC1080()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='sgp40.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sgp40._logger = logging.getLogger('ecomet.spg40')
sgp40._logger.info('Start logging ...')

(temp,hmdt, ret) = sens.both_measurement()

#If you want to modify the environment parameters, you can do so
#elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
sgp40.set_envparams(relative_humidity = hmdt,temperature_c = temp)
sgp40._logger.info('temp: %.2f hmdt: %.2f'%(temp,hmdt))

while True:
    # get raw vlaue
    sgp40._logger.info('Raw vlaue: %d'%(sgp40.measure_raw()))
    sleep(1)
