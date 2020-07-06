#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.hdc1080_pkg import hdc1080
import logging
#from  i2c_pkg.pca9632_pkg import pca9632_constant

sens = hdc1080.HDC1080()

logging.basicConfig(level=logging.DEBUG,  # change level looging to (INFO, DEBUG, ERROR)
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

#print ('{}'.format(sens._address))

#15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
# 0  0  0  1  0  1  1  0  0  0  0  0  0  0  0  0
# 00010110 00000000
# 1600
# MODE_BOTH = Temperaturea nd Humidityare acquiredin sequence,Temperature first.
# HRES_RES3 = humidity 8 bit
# TRES_RES2 = temperature 11 bit

ret = sens.write_register ( register = 'CONF', bits = ['RST_ON']);
sens._logger.info('CONF Write correct') if ret == 0 else sens._logger.error('Write error %s'.format(ret))

(val,ret) = sens.serial()
sens._logger.info('SERIAL Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('SER ID: %s',format(val))

(val,ret) = sens.manufacturer()
sens._logger.info('MANUFACTURER Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('MAN ID: %s',format(val))

(val,ret) = sens.deviceid()
sens._logger.info('DEVICE Read correct') if ret == 0 else sens._logger.error('Read error %s'.format(ret))
sens._logger.info('DEV ID: %s',format(val))
     
     

#reg_battery = sens.battery();
#print ("{}".format(reg_view));

'''
print("Current Status")
reg_view = pca9632.read_pca9632();
print ("{}".format(reg_view));

print ("SW Reset")
ret = pca9632.software_reset()
ret = pca9632.ledout_clear()
print ("Reset correct") if ret == 0 else print ("Reset error")
reg_view = pca9632.read_pca9632();
print ("{}".format(reg_view));

print ("MODE1 => (ALLCALL,SLEEP)")
ret = pwm.write_register( register = 'MODE1', bits = ['ALLCALL','SLEEP'])
#ret = pwm.write_register( register = 'MODE1', bits = ['SUB1_N','SUB2_N','SUB3_N'])
print("MODE1 Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("MODE2 => (OUTDRV,INVRT,DMBLNK_BLINKING)")
ret = pwm.write_register( register = 'MODE2', bits = ['OUTDRV','INVRT','DMBLNK_BLINKING'])
print("MODE2 Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("MODE2 => (INVRT_N)")
ret = pwm.write_register( register = "MODE2", bits = ['INVRT_N'])
print("MODE2 Wriete correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("LEDOUT => (LDR0->ON, LDR1->GRPPWM, LDR3->PWM)")
print ("LEDOUT => 1011 0001 => 1->13->13->141");
ret = pwm.write_register( register = 'LEDOUT', bits = [{'LDR0' : 'PWM' }, {'LDR1' : 'PWM_GRPPWM'}, {'LDR2' : 'OFF'}, {'LDR3' : 'PWM'}])
print("LEDOUT Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("PWM0 set to 50%")
ret = pwm.write_register( register = 'PWM0', bits = [{'PWM' : '101' }])
print("PWM0 Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("PWM1 set to 100%")
ret = pwm.write_register( register = 'PWM1', bits = [{'GRPPWM' : 0xFF }])
print("PWM1 Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("PWM2 set to 100%")
ret = pwm.write_register( register = 'PWM2', bits = [{'GRPPWM' : 0xFF }])
print("PWM2 Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))

print ("PWM3 set to 100%")
ret = pwm.write_register( register = 'PWM3', bits = [{'PWM' : 0xFF }])
print("PWM3 Write correct") if ret ==0 else print ("Write error")
reg_view = pca9632.read_pca9632()
print ("{}".format(reg_view))
'''
