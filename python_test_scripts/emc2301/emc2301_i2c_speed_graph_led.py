#!/usr/bin/env python3

from  i2c_pkg.emc2301_pkg import emc2301
from  i2c_pkg.pca9632_pkg import pca9632
from i2c_pkg.emc2301_pkg import fan_type
import logging
import statistics

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

fan_list = emc2301.fan_list
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
    
(val,ret) = sens.productid()
sens._logger.info('PRODUCT Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('PRODUCT ID: %s',format(val))

(val,ret) = sens.manufid()
sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MANUF ID: %s',format(val))

(val,ret) = sens.revisionid()
sens._logger.info('REVISION Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('REVISION ID: %s',format(val))

ret = pca9632.software_reset()
ret = pca9632.ledout_clear()
ret = pwm.write_register( register = 'MODE1', bits = ['ALLCALL','SLEEP_N'])
ret = pwm.write_register( register = 'MODE2', bits = ['DMBLNK_BLINKING'])
ret = pwm.write_register( register = 'LEDOUT', bits = [{'LDR0' : 'OFF' }, {'LDR1' : 'PWM'}, {'LDR2' : 'PWM'}, {'LDR3' : 'PWM'}])
#pwm.write_register( register = 'GRPPWM', bits = [{ 'GRPPWM' : 0 }] )


sens.write_register(register = 'FAN_CONF2', bits = ['EN_RRC'])
sens.write_register(register = 'FAN_SETTING', value = 0)
sens.write_register(register = 'FAN_CONF1', bits = ['EN_ALGO_CLR'])
ret = sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE_500_1'] )
ret = sens.write_register(register = 'FAN_CONF1', bits = ['EDGES'], bit = fan_list['EDGES_5_2POLE_1'] )
print ('RET: {}'.format(ret))
from time import sleep

speed = 0 #16
rgb (rblue)
while speed <= 255 :
   measure = []
   if (speed == 26 ) : rgb(green)
   elif (speed == 50 ) : rgb(violet)
   elif (speed == 75 ) : rgb(cyan)
   elif (speed == 100 ) : rgb(rose)
   elif (speed == 125 ) : rgb(orange)
   elif (speed == 150 ) : rgb(azure)
   elif (speed == 175 ) : rgb(red)
   elif (speed == 200 ) : rgb(yellow)
   elif (speed == 225 ) : rgb(magenta)
   elif (speed == 250 ) : rgb(springg)
#   elif (speed == 255 ) : rgb(chartre)

   for i in range (10) :
     measure.append(sens.speed()[0])   
     sleep(0.5)
   print ('{}:{}'.format(speed,int(statistics.mean(measure))))
   sens.write_register(register = 'FAN_SETTING', value = speed)
   speed = speed + 1

