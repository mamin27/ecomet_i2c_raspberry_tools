#!/usr/bin/env python3

import pca9632
import pca9632_constant

def read_pca9632() :
   
   register = {}

   mode1_bit_list = { 'SLEEP' : pca9632_constant.SLEEP,
                      'SUB1' : pca9632_constant.SUB1,
                      'SUB2' : pca9632_constant.SUB2,
                      'SUB3' : pca9632_constant.SUB3,
                      'ALLCALL' : pca9632_constant.ALLCALL }
             
   reg_mode1 = {}
   reg_mode2 = {}
   reg_ledout = {}
   
   reg_mode1['ALLCALL'] = 'ON' if pwm.read_register( register = 'MODE1' ) & mode1_bit_list['ALLCALL'] > 0  else 'OFF'
   reg_mode1['SUB3'] = 'ON' if pwm.read_register( register = 'MODE1' ) & mode1_bit_list['SUB3'] > 0 else 'OFF'      
   reg_mode1['SUB2'] = 'ON' if pwm.read_register( register = 'MODE1' ) & mode1_bit_list['SUB2'] > 0 else 'OFF'      
   reg_mode1['SUB1'] = 'ON' if pwm.read_register( register = 'MODE1' ) & mode1_bit_list['SUB1'] > 0 else 'OFF'      
   reg_mode1['SLEEP'] = 'ON' if pwm.read_register( register = 'MODE1' ) & mode1_bit_list['SLEEP'] > 0 else 'OFF'
      
   register['MODE1'] = reg_mode1
   
   mode2_bit_list = { 'DMBLNK' : pca9632_constant.DMBLNK,
                      'INVRT' : pca9632_constant.INVRT,
                      'OCH' : pca9632_constant.OCH,
                      'OUTDRV' : pca9632_constant.OUTDRV }             
   
   reg_mode2['OUTDRV'] = 'ON' if pwm.read_register( register = 'MODE2' ) & mode2_bit_list['OUTDRV'] > 0 else 'OFF'
   reg_mode2['OCH'] = 'ON' if pwm.read_register( register = 'MODE2' ) & mode2_bit_list['OCH'] > 0 else 'OFF'
   reg_mode2['INVRT'] = 'ON' if pwm.read_register( register = 'MODE2' ) & mode2_bit_list['INVRT'] > 0 else 'OFF'
   reg_mode2['DMBLNK'] = 'ON' if pwm.read_register( register = 'MODE2' ) & mode2_bit_list['DMBLNK'] > 0 else 'OFF'
   
   register['MODE2'] = reg_mode2

   register['PWM0'] = round(pwm.read_register( register = 'PWM0' ) / 255 * 100,1)
   register['PWM1'] = round(pwm.read_register( register = 'PWM1' ) / 255 * 100,1)
   register['PWM2'] = round(pwm.read_register( register = 'PWM2' ) / 255 * 100,1)
   register['PWM3'] = round(pwm.read_register( register = 'PWM3' ) / 255 * 100,1)
   register['GRPPWM'] = round(pwm.read_register( register = 'GRPPWM' ) / 255 * 100,1)
   register['GRPFREQ'] = str(round(1/ (pwm.read_register( register = 'GRPFREQ' ) + 1 / 24),1)) + ' Hz' if reg_mode2['DMBLNK'] == 'ON' else '0 Hz' 
   
   reg_ledout_list = { 'LDR0' : pca9632_constant.LDR0,
                       'LDR1' : pca9632_constant.LDR1,
                       'LDR2' : pca9632_constant.LDR2,
                       'LDR3' : pca9632_constant.LDR3 }
                       
   ledout_mode = { 'OFF' : pca9632_constant.OFF,
                   'ON'  : pca9632_constant.ON,
                   'PWM' : pca9632_constant.PWM,
                   'PWM_GRPPWM' : pca9632_constant.PWM_GRPPWM }
                   
   ldr0 = pwm.read_register( register = 'LEDOUT' ) & 0x03 
   ldr1 = (pwm.read_register( register = 'LEDOUT' ) & 0x0c) >> 2
   ldr2 = (pwm.read_register( register = 'LEDOUT' ) & 0x30) >> 4
   ldr3 = (pwm.read_register( register = 'LEDOUT' ) & 0xc0) >> 6
   
   if ldr0 == ledout_mode ['OFF'] :
      reg_ledout['LDR0'] = 'OFF'
   elif ldr0 == ledout_mode ['ON'] :
      reg_ledout['LDR0'] = 'ON'
   elif ldr0 == ledout_mode ['PWM'] :
      reg_ledout['LDR0'] = 'PWM'
   elif ldr0 == ledout_mode ['PWM_GRPPWM'] :
      reg_ledout['LDR0'] = 'PWM_GRPPWM'

   if ldr1 == ledout_mode ['OFF'] :
      reg_ledout['LDR1'] = 'OFF'
   elif ldr1 == ledout_mode ['ON'] :
      reg_ledout['LDR1'] = 'ON'
   elif ldr1 == ledout_mode ['PWM'] :
      reg_ledout['LDR1'] = 'PWM'
   elif ldr1 == ledout_mode ['PWM_GRPPWM'] :
      reg_ledout['LDR1'] = 'PWM_GRPPWM'
     
   if ldr2 == ledout_mode ['OFF'] :
      reg_ledout['LDR2'] = 'OFF'
   elif ldr2 == ledout_mode ['ON'] :
      reg_ledout['LDR2'] = 'ON'
   elif ldr2 == ledout_mode ['PWM'] :
      reg_ledout['LDR2'] = 'PWM'
   elif ldr2 == ledout_mode ['PWM_GRPPWM'] :
      reg_ledout['LDR2'] = 'PWM_GRPPWM'
     
   if ldr3 == ledout_mode ['OFF'] :
      reg_ledout['LDR3'] = 'OFF'
   elif ldr3 == ledout_mode ['ON'] :
      reg_ledout['LDR3'] = 'ON'
   elif ldr3 == ledout_mode ['PWM'] :
      reg_ledout['LDR3'] = 'PWM'
   elif ldr3 == ledout_mode ['PWM_GRPPWM'] :
      reg_ledout['LDR3'] = 'PWM_GRPPWM'
      
      
   register['SUBADR1'] = str(hex((pwm.read_register( register = 'SUBADR1' ) & 0xFE) >> 1))
   register['SUBADR2'] = str(hex((pwm.read_register( register = 'SUBADR2' ) & 0xFE) >> 1))
   register['SUBADR3'] = str(hex((pwm.read_register( register = 'SUBADR3' ) & 0xFE) >> 1))
   
   register['LEDOUT'] = reg_ledout
   
   register['ALLCALLADR'] = str(hex((pwm.read_register( register = 'ALLCALLADR' ) & 0xFE) >> 1))
   
   return (register)
      
if __name__ == "__main__":

   pwm = pca9632.PCA9632()

   reg_view = read_pca9632();
   print ("{}".format(reg_view));
   
   print ("MODE1 => (ALLCALL_N,SLEEP_N)\n")
   ret = pwm.write_register( register = 'MODE1', bits = ['SUB1','SLEEP_N'] )
   print ("MODE1 Write correct\n") if ret == 0 else print ("Write error\n")
   reg_view = read_pca9632();
   print ("{}".format(reg_view));
   
   print ("MODE2 => (OUTDRV,INVRT)\n")
   ret = pwm.write_register( register = 'MODE2', bits = ['OUTDRV','INVRT'] )
   print ("MODE2 Write correct\n") if ret == 0 else print ("Write error\n")
   reg_view = read_pca9632();
   print ("{}".format(reg_view));
   
   print ("MODE2 => (INVRT_N)\n")
   ret = pwm.write_register( register = 'MODE2', bits = ['INVRT_N'] )
   print ("MODE2 Write correct\n") if ret == 0 else print ("Write error\n")
   reg_view = read_pca9632();
   print ("{}".format(reg_view));
   
   print ("LEDOUT => (LDR0->ON,LDR3->PWM)\n")
   ret = pwm.write_register( register = 'LEDOUT', bits = [{'LDR0' : 'ON' }, {'LDR1' : 'PWM_GRPPWM'}, {'LDR2' : 'OFF'}, {'LDR3' : 'PWM'}] )
   print ("LEDOUT Write correct\n") if ret == 0 else print ("Write error\n")
   reg_view = read_pca9632();
   print ("{}".format(reg_view));
