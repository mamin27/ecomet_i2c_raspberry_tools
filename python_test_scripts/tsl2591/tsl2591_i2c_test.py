#!/usr/bin/env python3

import sys,os
sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  tsl2591 import tsl2591,tsl2591_constant
#from  ecomet_i2c_sensors.tsl2591 import tsl2591
import logging

sens = tsl2591.TSL2591()

logging.basicConfig(level=logging.DEBUG,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='tsl2591.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.tsl2591')
sens._logger.info('Start logging ...')

print(tsl2591.conf_register_list())
print('enable ic')
sens.enable_ic()
print(tsl2591.conf_register_list())
sens.disable_ic()
print(tsl2591.conf_register_list())

sens.write_register('THR_AI',117835020)
sens.write_register('THR_NPAI',185207049)
sens.reset_ic()

print('Gain: ',sens.get_gain())
print('IntegralTime: ',sens.get_IntegralTime())

sens.set_gain('GAIN_MAX')
print(tsl2591.conf_register_list())
sens.set_IntegralTime('TIME_500MS')
print(tsl2591.conf_register_list())
#sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))

#ret = sens.battery()
#sens._logger.info('Battery > 2.4V, correct') if ret == 0 else sens._logger.error('Battery < 2.4V, error')

#15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
# 0  0  0  1  0  1  1  0  0  0  0  0  0  0  0  0
# 00010110 00000000
# 1600
# MODE_BOTH = Temperaturea nd Humidityare acquiredin sequence,Temperature first.
# HRES_RES3 = humidity 8 bit (10)
# TRES_RES2 = temperature 11 bit

#ret = sens.write_register( register = 'CONF', bits = ['MODE_BOTH','HRES_RES1','TRES_RES1'])
#sens._logger.info('Write CONF register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

#(val,ret) = sens.serial()
#sens._logger.info('SERIAL Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
#sens._logger.info('SER ID: %s',format(val))

#(val,ret) = sens.manufacturer()
#sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
#sens._logger.info('MAN ID: %s',format(val))

#(val,ret) = sens.deviceid()
#sens._logger.info('DEVICE Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
#sens._logger.info('DEV ID: %s',format(val))
#register = hdc1080.register_list()
#print ('{}'.format(register))

#(temp,hmdt, ret) = sens.both_measurement()
#if ret == 0 :
#    sens._logger.info('Measured Temperate BOTH: %s \u2103','{0:10.2f}'.format(temp))
#    sens._logger.info('Measured Humidity BOTH: %s %s','{0:10.2f}'.format(hmdt),'%') 
#else :
#    sens._logger.error('Read error %s'.format(ret))
    
#15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
# 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
# 00010110 00000000
# 1600
# MODE_ONLY = temperature or humidity is acquired
# HRES_RES1 = humidity 14 bit (10)
# TRES_RES1 = temperature 14 bit

#ret = sens.sw_reset()
#sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))
#ret = sens.write_register( register = 'CONF', bits = ['MODE_ONLY','HRES_RES1','TRES_RES1'])
#sens._logger.info('Write CONF register correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))
#register = hdc1080.register_list()
#print ('{}'.format(register))

#(temp, ret) = sens.measure_temp()
#if ret == 0 :
#    sens._logger.info('Measured Temperate IND: %s \u2103','{0:10.2f}'.format(temp))
#else :
#    sens._logger.error('Read error %s'.format(ret))

#(hmdt, ret) = sens.measure_hmdt()
#if ret == 0 :
#    sens._logger.info('Measured Humidity IND: %s %s','{0:10.2f}'.format(hmdt),'%')
#else :
#    sens._logger.error('Read error %s'.format(ret))

##########################################################
#ret = sens.sw_reset()
#sens._logger.info('SW Reset correct') if ret == 0 else sens._logger.error('SW Reset error %s'.format(ret))

#ret = sens.battery()
#sens._logger.info('Battery > 2.4V, correct') if ret == 0 else sens._logger.error('Battery < 2.4V, error')
#ret = sens.write_register( register = 'CONF', bits = ['TRES_RES2','HRES_RES2','MODE_ONLY','HEAT_DISABLE'])
#register = hdc1080.register_list()
#print ('{}'.format(register))
#(measure,ret) = hdc1080.measure_list()

#if ret == 0 :
#    print('{}'.format(measure))
#else :
#    sens._logger.error('Measure Read error %s'.format(ret))