#!/usr/bin/python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.sgp40 import sgp40
from  ecomet_i2c_sensors.hdc1080 import hdc1080
import logging
from time import sleep

#set IICbus elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
sgp = sgp40.SGP40()
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
sgp._logger = logging.getLogger('ecomet.spg40')
sgp._logger.info('Start logging ...')

(temp,hmdt, ret) = sens.both_measurement()

#set Warm-up time
sgp._logger.info('Please wait 10 seconds...')
sgp.begin(10)

#If you want to modify the environment parameters, you can do so
#elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
sgp.set_envparams(relative_humidity = hmdt,temperature_c = temp)
sgp._logger.info('temp: %.2f hmdt: %.2f'%(temp,hmdt))

while True:
    idx = sgp.get_voc_index()
    sgp._logger.info('Voc index : %d  [%s]'%(idx, sgp.index_to_explanation(index = idx)))
    sleep(1)
