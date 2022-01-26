#!/usr/bin/env python3
# test script for RGB LED testing, in loop color will be rotated in palette and dimmed

import sys
import time
print (sys.version)
from  ecomet_i2c_sensors.pca9632 import pca9632

pwm = pca9632.PCA9632()
reg_view = pca9632.read_pca9632();
ret = pca9632.software_reset()
ret = pca9632.ledout_clear()
ret = pwm.write_register( register = 'MODE1', bits = ['ALLCALL','SLEEP_N'])
ret = pwm.write_register( register = 'MODE2', bits = ['DMBLNK_BLINKING'])
ret = pwm.write_register( register = 'LEDOUT', bits = [{'LDR0' : 'OFF' }, {'LDR1' : 'PWM'}, {'LDR2' : 'PWM'}, {'LDR3' : 'PWM'}])

# RGB led connected to PWM1, PWM2, PWM3
# PWM1 = BLUE, PWM2 = GREEN, PWM3 = RED

blue    = { 'R': 0,
            'G': 0,
            'B': 255 }
violet  = { 'R': 128,
            'G': 0,
            'B': 255 }
magenta = { 'R': 255,
            'G': 0,
            'B': 255 }
rose    = { 'R': 255,
            'G': 0,
            'B': 128 }
red     = { 'R': 255,
            'G': 0,
            'B': 0 }
orange  = { 'R': 255,
            'G': 128,
            'B': 0 }
yellow  = { 'R': 255,
            'G': 255,
            'B': 0 }
chartre = { 'R': 128,
            'G': 255,
            'B': 0 }
green   = { 'R': 0,
            'G': 255,
            'B': 0 }
springg = { 'R': 0,
            'G': 255,
            'B': 128 }
cyan    = { 'R': 0,
            'G': 255,
            'B': 255 }
azure   = { 'R': 0,
            'G': 128,
            'B': 255 }
            
der = [1,2,4,8,10,12,14,16,18,20]
            

palette = [blue,violet,magenta,rose,red,orange,yellow,chartre,green,springg,cyan,azure]
from time import sleep
for loop in range (1,10) :
 for i in palette :
	 
   pwm.write_register( register = 'PWM3', bits = [{'PWM' : int(i['R'] / der[loop]) }])
   pwm.write_register( register = 'PWM2', bits = [{'PWM' : int(i['G'] / der[loop]) }])
   pwm.write_register( register = 'PWM1', bits = [{'PWM' : int(i['B'] / der[loop]) }])
   sleep(0.1)
   
pwm.write_register( register = 'PWM3', bits = [{'PWM' : '0' }])
pwm.write_register( register = 'PWM2', bits = [{'PWM' : '0' }])
pwm.write_register( register = 'PWM1', bits = [{'PWM' : '0' }])

   
