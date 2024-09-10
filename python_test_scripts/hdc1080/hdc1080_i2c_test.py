#!/usr/bin/env python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.hdc1080 import hdc1080
import logging

sens = hdc1080.HDC1080(busnum=0)

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

(val,ret) = sens.serial()
sens._logger.info('SERIAL Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('SER ID: %s',format(val))

(val,ret) = sens.manufacturer()
sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MAN ID: %s',format(val))

(val,ret) = sens.deviceid()
sens._logger.info('DEVICE Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('DEV ID: %s',format(val))

ret = sens.write_register( register = 'CONF', bits = [{'MODE':'BOTH'},{'HRES':'14'},{'TRES':'14'}])
sens._logger.info('Write CONF register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

register = hdc1080.register_list()
print ('{}'.format(register))

(temp,hmdt, ret) = sens.both_measurement()
if ret == 0 :
    sens._logger.info('Measured Temperate BOTH: %s \u2103','{0:10.2f}'.format(temp))
    sens._logger.info('Measured Humidity BOTH: %s %s','{0:10.2f}'.format(hmdt),'%') 
else :
    sens._logger.error('Read error %s'.format(ret))

ret = sens.sw_reset()
sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))
ret = sens.write_register( register = 'CONF', bits = [{'MODE':'ONLY'},{'HRES':'11'},{'TRES':'11'}])
sens._logger.info('Write CONF register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))
register = hdc1080.register_list()
print ('{}'.format(register))

(temp, ret) = sens.measure_temp()
if ret == 0 :
    sens._logger.info('Measured Temperate IND: %s \u2103','{0:10.2f}'.format(temp))
else :
    sens._logger.error('Read error %s'.format(ret))

ret = sens.write_register( register = 'CONF', bits = [{'MODE':'BOTH'},{'HRES':'11'},{'TRES':'11'}])
(hmdt, ret) = sens.measure_hmdt()
if ret == 0 :
    sens._logger.info('Measured Humidity IND: %s %s','{0:10.2f}'.format(hmdt),'%')
else :
    sens._logger.error('Read error %s'.format(ret))

##########################################################
ret = sens.sw_reset()
sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))

ret = sens.battery()
sens._logger.info('Battery > 2.4V, correct') if ret == 0 else sens._logger.error('Battery < 2.4V, error')
ret = sens.write_register( register = 'CONF', bits = [{'TRES':'11'},{'HRES':'08'},{'MODE':'ONLY'},{'HEAT':'ENABLE'}])
register = hdc1080.register_list()
print ('{}'.format(register))
(measure,ret) = hdc1080.measure_list()

if ret == 0 :
    print('{}'.format(measure))
else :
    sens._logger.error('Measure Read error %s'.format(ret))
