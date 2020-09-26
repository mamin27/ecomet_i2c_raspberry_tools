#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.emc2301_pkg import emc2301
from i2c_pkg.emc2301_pkg import fan_type
import logging

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

ret = sens.self_test()
if ret == 0 :
    print(":TEST_PASSED:")
else :
    print(":MISSING_CHIP:")
    
(val,ret) = sens.productid()
sens._logger.info('PRODUCT Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('PRODUCT ID: %s',format(val))

(val,ret) = sens.manufid()
sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MANUF ID: %s',format(val))

(val,ret) = sens.revisionid()
sens._logger.info('REVISION Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('REVISION ID: %s',format(val))

sens.write_register(register = 'FAN_CONF2', bits = ['EN_RRC'])

register = emc2301.conf_register_list()
print ('{}'.format(register))

while True :
   print ('---------------------------------')
   sens.write_register(register = 'FAN_SETTING', bits = [0])
   sens.write_register(register = 'FAN_CONF1', bits = ['EN_ALGO_CLR'])
   sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE'] )
   #sens.write_register(register = 'FAN_SETTING', bits = [20])
   #sens.write_register(register = 'TACH_TARGET', bits = [33])
   from time import sleep
   print('Speed: 0')
   for i in range (10) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   sens.write_register(register = 'FAN_SETTING', bits = [50])
   from time import sleep
   print ('Speed: 50')
   for i in range (20) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   sens.write_register(register = 'FAN_SETTING', bits = [100])
   from time import sleep
   print ('Speed: 100')
   for i in range (20) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   register = emc2301.conf_register_list()
   #print ('{}'.format(register))
   sens.write_register(register = 'FAN_SETTING', bits = [160])
   print('Speed: 160')
   for i in range (13) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   register = emc2301.conf_register_list()
   #print ('{}'.format(register))
   sens.write_register(register = 'FAN_SETTING', bits = [200])
   print('Speed: 200')
   for i in range (20) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   register = emc2301.conf_register_list()
   #print ('{}'.format(register))
   sens.write_register(register = 'FAN_SETTING', bits = [255])
   print ('Speed: 255')
   for i in range (20) :
     sleep(1)
     register = sens.speed()[0]
     print ('{}'.format(register))

   print ('---------------------------------')

