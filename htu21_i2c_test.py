#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.htu21_pkg import htu21 
import logging

sens = htu21.HTU21()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='htu21.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.htu21')
sens._logger.info('Start logging ...')

ret = sens.sw_reset()
sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))

ret = sens.battery()
sens._logger.info('Battery > 2.4V, correct') if ret == 0 else sens._logger.error('Battery < 2.4V, error')

ret = sens.write_register( register = 'WRITE_USER', bits = ['MEAS_RES1','HEAT_DISABLE'])
sens._logger.info('Write WRITE_REG register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

register = htu21.register_list()
print ('{}'.format(register))

(temp, ret) = sens.measure_temp()
if ret == 0 :
    sens._logger.info('Measured Temperate IND: %s \u2103','{0:10.2f}'.format(temp))
else :
    sens._logger.error('Read error %s'.format(ret))
(hmdt, ret) = sens.measure_hmdt()
if ret == 0 :
    sens._logger.info('Measured Humidity IND: %s %s','{0:10.2f}'.format(hmdt),'%')
else :
    sens._logger.error('Read error %s'.format(ret))
    
##############################################################

ret = sens.write_register( register = 'WRITE_USER', bits = ['MEAS_RES4','HEAT_DISABLE'])
sens._logger.info('Write WRITE_REG register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

register = htu21.register_list()
print ('{}'.format(register))

(temp, ret) = sens.measure_temp()
if ret == 0 :
    sens._logger.info('Measured Temperate IND: %s \u2103','{0:10.2f}'.format(temp))
else :
    sens._logger.error('Read error %s'.format(ret))
(hmdt, ret) = sens.measure_hmdt()
if ret == 0 :
    sens._logger.info('Measured Humidity IND: %s %s','{0:10.2f}'.format(hmdt),'%')
else :
    sens._logger.error('Read error %s'.format(ret))

##############################################################

(measure,ret) = htu21.measure_list()

if ret == 0 :
    print('{}'.format(measure))
else :
    sens._logger.error('Measure Read error %s'.format(ret))

###############################################################

(dew_point,ret) = sens.dew_point()

if ret == 0 :
    sens._logger.info('Calculated Dew Point IND: %s \u2103','{0:10.2f}'.format(dew_point))
else :
    sens._logger.error('Dew_point Read error %s'.format(ret))
