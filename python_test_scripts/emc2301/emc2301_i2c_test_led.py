#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.emc2301_pkg import emc2301
from  i2c_pkg.pca9632_pkg import pca9632
from i2c_pkg.emc2301_pkg import fan_type
import logging

# RGB led connected to PWM1, PWM2, PWM3
# PWM1 = BLUE, PWM2 = GREEN, PWM3 = RED
# http://www.elumtools.com/docs/2017/Content/Using%20ElumTools/Luminance%20Color.htm

rblue   = { 'R': 8,			#lamda 460
            'G': 0,
            'B': 255,
            'pallete': 'royal blue' }
violet  = { 'R': 128,		#
            'G': 0,
            'B': 255,
            'pallete':'violet' }
magenta = { 'R': 255,		#
            'G': 0,
            'B': 255,
            'pallete':'magenta' }
rose    = { 'R': 232,		#
            'G': 64,
            'B': 170,
            'pallete':'rose' }
red     = { 'R': 255,		#lamda 615
            'G': 0,
            'B': 8,
            'pallete':'red' }
orange  = { 'R': 255,		#lamda 595
            'G': 70,
            'B': 0,
            'pallete':'orange' }
yellow  = { 'R': 255,		#
            'G': 255,
            'B': 9,
            'pallete':'yellow' }
chartre = { 'R': 133,		#lamda 570
            'G': 255,
            'B': 0,
            'pallete':'chartreuse green' }
green   = { 'R': 0,			#lamda 550
            'G': 255,
            'B': 0,
            'pallete':'green' }
springg = { 'R': 0,			#lamda 545
            'G': 255,
            'B': 25,
            'pallete':'spring green' }
cyan    = { 'R': 0,			#lamda 495 
            'G': 255,
            'B': 215,
            'pallete':'cyan' }
azure   = { 'R': 0,			#lamda 480
            'G': 111,
            'B': 255,
            'pallete':'azure' }

palette = [rblue,violet,magenta,rose,red,orange,yellow,chartre,green,springg,cyan,azure]

def rgb (color) :

   position = palette.index(color)
   i = palette[position]
   print ('LED color: {}'.format(color['pallete']))

   #pwm.write_register( register = 'PWM3', bits = [{'PWM' : int(i['R']) }])
   #pwm.write_register( register = 'PWM2', bits = [{'PWM' : int(i['G']) }])
   #pwm.write_register( register = 'PWM1', bits = [{'PWM' : int(i['B']) }])
   #china RGB
   pwm.write_register( register = 'PWM2', bits = [{'PWM' : int(i['R']) }])
   pwm.write_register( register = 'PWM3', bits = [{'PWM' : int(i['G']) }])
   pwm.write_register( register = 'PWM1', bits = [{'PWM' : int(i['B']) }])

   return 0


fan_list = { 'RANGE' : fan_type.RANGE , 'EDGES' : fan_type.EDGES }

sens = emc2301.EMC2301()
pwm = pca9632.PCA9632()
reg_view = pca9632.read_pca9632();

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
   sens.write_register(register = 'FAN_SETTING', value = 0)
   sens.write_register(register = 'FAN_CONF1', bits = ['EN_ALGO_CLR'])
   sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE'] )
   #sens.write_register(register = 'FAN_SETTING', bits = [20])
   #sens.write_register(register = 'TACH_TARGET', bits = [33])
   from time import sleep
   print('Speed: 0')
   rgb (rblue)
   for i in range (10) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   sens.write_register(register = 'FAN_SETTING', value = 50)
   from time import sleep
   print ('Speed: 50')
   rgb (green)
   for i in range (20) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   sens.write_register(register = 'FAN_SETTING', value = 100)
   from time import sleep
   print ('Speed: 100')
   rgb (violet)
   for i in range (20) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   register = emc2301.conf_register_list()
   #print ('{}'.format(register))
   sens.write_register(register = 'FAN_SETTING', value = 160)
   print('Speed: 160')
   rgb (cyan)
   for i in range (13) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   register = emc2301.conf_register_list()
   #print ('{}'.format(register))
   sens.write_register(register = 'FAN_SETTING', value = 200)
   print('Speed: 200')
   rgb (red)
   for i in range (20) :
     register = sens.speed()[0]
     print ('{}'.format(register))
     sleep(1)
   register = emc2301.conf_register_list()
   #print ('{}'.format(register))
   sens.write_register(register = 'FAN_SETTING', value = 255)
   print ('Speed: 255')
   rgb (springg)
   for i in range (20) :
     sleep(1)
     register = sens.speed()[0]
     print ('{}'.format(register))

   print ('---------------------------------')

