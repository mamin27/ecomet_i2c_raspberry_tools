#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.ms5637_pkg import ms5637
import logging

sens = ms5637.MS5637()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='ms5637.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.ms5637')
sens._logger.info('Start logging ...')

ret = sens.sw_reset()
sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))

#C1 = sens.read_register('PROM_PRE_SENS')    first possibility how to read C1
#C1 = sens.c1[0]							 second possbility how to read C1

# first way to calculate temperature
#sens.write_register('D2_CONV_256', stime = sens.d1_time)
#D2 = sens.read_register('ADC_READ')[0]
#dT = D2 - C5 * 2**8
#temp = 2000 + dT * C6 / 2**23
#print ("d2 = {}".format(D2))
#print ("dT = {}".format(dT))
#print ("TEMP = {}".format(temp))

data = sens.measure (accuracy = 6)
temp = data[0]
temp_f = data[1]
pressure = data[2]
sens._logger.info('Pressure = %s mbar','{0:10.2f}'.format(pressure))
sens._logger.info('Temperature in Celsius = %s \u2103','{0:10.2f}'.format(temp))
sens._logger.info('Temperature in Fahrenheit = %s F','{0:10.2f}'.format(temp_f))
