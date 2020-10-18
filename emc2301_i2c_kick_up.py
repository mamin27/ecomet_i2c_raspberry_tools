#!/usr/bin/env python3

from  i2c_pkg.emc2301_pkg import emc2301
from i2c_pkg.emc2301_pkg import fan_type
import logging
import statistics

fan_list = { 'RANGE' : fan_type.RANGE , 'EDGES' : fan_type.EDGES }
sens = emc2301.EMC2301()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='emc2301.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.emc2301')
sens._logger.info('Start logging ...')
    
(val,ret) = sens.productid()
sens._logger.info('PRODUCT Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('PRODUCT ID: %s',format(val))

(val,ret) = sens.manufid()
sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MANUF ID: %s',format(val))

(val,ret) = sens.revisionid()
sens._logger.info('REVISION Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('REVISION ID: %s',format(val))

sens.write_register(register = 'FAN_SPIN_UP', bits = ['NOKICK'] )

register = emc2301.conf_register_list()
print ('{}'.format(register))

sens.write_register(register = 'FAN_CONF2', bits = ['EN_RRC'])

sens.write_register(register = 'FAN_SETTING', value = 0)
sens.write_register(register = 'FAN_MAX_STEP', value = 63)
sens.write_register(register = 'FAN_CONF1', bits = ['EN_ALGO_CLR'])
sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE'] )
sens.write_register(register = 'FAN_SPIN_UP', bits = ['NOKICK_CLR'] )
register = emc2301.conf_register_list()
print ('{}'.format(register))

from time import sleep
sleep(5)
sens.write_register(register = 'FAN_MAX_STEP', value = 63)

sample1 = []
sample1 = sens.fan_kick_up(10,0.001,3000,170)

sample2 = []
sample2 = sens.fan_kick_up(5,0.001,3000,100)

sample3 = []
sample3 = sens.fan_kick_up(5,0.001,4000,255)

sample = sample1 + sample2 + sample3

for index in range (0,10000) :
	print ('{}:{}'.format(index,sample[index]))
'''
speed = 16
while speed <= 255 :
   measure = []
   for i in range (10) :
     measure.append(sens.speed()[0])   
     sleep(0.5)
   print ('{}:{}'.format(speed,int(statistics.mean(measure))))
   sens.write_register(register = 'FAN_SETTING', bits = [speed])
   speed = speed + 1

'''
