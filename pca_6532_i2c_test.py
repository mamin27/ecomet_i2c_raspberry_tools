
#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.pca9632_pkg import pca9632
#from  i2c_pkg.pca9632_pkg import pca9632_constant

pwm = pca9632.PCA9632()

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
