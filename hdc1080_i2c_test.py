#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.hdc1080_pkg import hdc1080
import logging
#from  i2c_pkg.pca9632_pkg import pca9632_constant

sens = hdc1080.HDC1080()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='hdc1080.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.hdc1080')
sens._logger.info('Start logging ...')

ret = sens.sw_reset()
sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))

ret = sens.battery()
sens._logger.info('Battery > 2.4V, correct') if ret == 0 else sens._logger.error('Battery < 2.4V, error')

#15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
# 0  0  0  1  0  1  1  0  0  0  0  0  0  0  0  0
# 00010110 00000000
# 1600
# MODE_BOTH = Temperaturea nd Humidityare acquiredin sequence,Temperature first.
# HRES_RES3 = humidity 8 bit (10)
# TRES_RES2 = temperature 11 bit

ret = sens.write_register( register = 'CONF', bits = ['MODE_BOTH','HRES_RES3','TRES_RES2'])
sens._logger.info('Write CONF register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

(val,ret) = sens.serial()
sens._logger.info('SERIAL Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('SER ID: %s',format(val))

(val,ret) = sens.manufacturer()
sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MAN ID: %s',format(val))

(val,ret) = sens.deviceid()
sens._logger.info('DEVICE Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('DEV ID: %s',format(val))

(temp,hmdt, ret) = sens.both_measurement()
if ret == 0 :
    sens._logger.info('Measured Temperate BOTH: %s \u2103','{0:10.2f}'.format(temp))
    sens._logger.info('Measured Humidity BOTH: %s %s','{0:10.2f}'.format(hmdt),'%') 
else :
    sens._logger.error('Read error %s'.format(ret))
    
#15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
# 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
# 00010110 00000000
# 1600
# MODE_ONLY = temperature or humidity is acquired
# HRES_RES1 = humidity 14 bit (10)
# TRES_RES1 = temperature 14 bit

ret = sens.write_register( register = 'CONF', bits = ['MODE_ONLY','HRES_RES1','TRES_RES1'])
sens._logger.info('Write CONF register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

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
