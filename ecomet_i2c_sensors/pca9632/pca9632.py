from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.pca9632 import pca9632_constant
#import pca9632_constant
#import i2c_command_oop



reg_list = { 'MODE1' : pca9632_constant.MODE1, 'MODE2' :  pca9632_constant.MODE2, 
             'PWM0' : pca9632_constant.PWM0, 'PWM1' : pca9632_constant.PWM1, 'PWM2' : pca9632_constant.PWM2, 'PWM3' : pca9632_constant.PWM3,
             'GRPPWM' : pca9632_constant.GRPPWM, 'GRPFREQ' : pca9632_constant.GRPFREQ, 'LEDOUT' : pca9632_constant.LEDOUT,
             'SUBADR1' : pca9632_constant.SUBADR1, 'SUBADR2' : pca9632_constant.SUBADR2, 'SUBADR3' : pca9632_constant.SUBADR3,
             'ALLCALLADR' : pca9632_constant.ALLCALLADR,
        }
mode1_bit_on_list = { 'SLEEP' : pca9632_constant.SLEEP,
                      'SUB1' : pca9632_constant.SUB1,
                      'SUB2' : pca9632_constant.SUB2,
                      'SUB3' : pca9632_constant.SUB3,
                      'ALLCALL' : pca9632_constant.ALLCALL
                }

mode1_bit_off_list = { 'SLEEP_N' : pca9632_constant.SLEEP_N,
                       'SUB1_N' : pca9632_constant.SUB1_N,
                       'SUB2_N' : pca9632_constant.SUB2_N,
                       'SUB3_N' : pca9632_constant.SUB3_N,
                       'ALLCALL_N' : pca9632_constant.ALLCALL_N
                }
                
mode2_bit_on_list = { 'DMBLNK_DIMMING' : pca9632_constant.DMBLNK_DIMMING,
                      'INVRT' : pca9632_constant.INVRT,
                      'OCH' : pca9632_constant.OCH,
                      'OUTDRV' : pca9632_constant.OUTDRV
                }

mode2_bit_off_list = { 'DMBLNK_BLINKING' : pca9632_constant.DMBLNK_BLINKING,
                       'INVRT_N' : pca9632_constant.INVRT_N,
                       'OCH_N' : pca9632_constant.OCH_N,
                       'OUTDRV_N' : pca9632_constant.OUTDRV_N
                }
                
led_bit_list = { 'LDR0' : pca9632_constant.LDR0_W,
                 'LDR1' : pca9632_constant.LDR1_W,
                 'LDR2' : pca9632_constant.LDR2_W,
                 'LDR3' : pca9632_constant.LDR3_W
                }

led_bit_mode = { 'OFF' : pca9632_constant.OFF,
                 'ON'  : pca9632_constant.ON,
                 'PWM' : pca9632_constant.PWM,
                 'PWM_GRPPWM' : pca9632_constant.PWM_GRPPWM
                }

logger = logging.getLogger(__name__)

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
   
   reg_mode1['ALLCALL'] = 'ON' if PCA9632().read_register( register = 'MODE1' ) & mode1_bit_list['ALLCALL'] > 0  else 'OFF'
   reg_mode1['SUB3'] = 'ON' if PCA9632().read_register( register = 'MODE1' ) & mode1_bit_list['SUB3'] > 0 else 'OFF'      
   reg_mode1['SUB2'] = 'ON' if PCA9632().read_register( register = 'MODE1' ) & mode1_bit_list['SUB2'] > 0 else 'OFF'      
   reg_mode1['SUB1'] = 'ON' if PCA9632().read_register( register = 'MODE1' ) & mode1_bit_list['SUB1'] > 0 else 'OFF'      
   reg_mode1['SLEEP'] = 'ON' if PCA9632().read_register( register = 'MODE1' ) & mode1_bit_list['SLEEP'] > 0 else 'OFF'
      
   register['MODE1'] = reg_mode1
   
   mode2_bit_list = { 'DMBLNK' : pca9632_constant.DMBLNK,
                      'INVRT' : pca9632_constant.INVRT,
                      'OCH' : pca9632_constant.OCH,
                      'OUTDRV' : pca9632_constant.OUTDRV }             
   
   reg_mode2['OUTDRV'] = 'ON' if PCA9632().read_register( register = 'MODE2' ) & mode2_bit_list['OUTDRV'] > 0 else 'OFF'
   reg_mode2['OCH'] = 'ON' if PCA9632().read_register( register = 'MODE2' ) & mode2_bit_list['OCH'] > 0 else 'OFF'
   reg_mode2['INVRT'] = 'ON' if PCA9632().read_register( register = 'MODE2' ) & mode2_bit_list['INVRT'] > 0 else 'OFF'
   reg_mode2['DMBLNK'] = 'DIMMING' if PCA9632().read_register( register = 'MODE2' ) & mode2_bit_list['DMBLNK'] > 0 else 'BLINKING'
   
   register['MODE2'] = reg_mode2
   
   reg_ledout_list = { 'LDR0' : pca9632_constant.LDR0,
                       'LDR1' : pca9632_constant.LDR1,
                       'LDR2' : pca9632_constant.LDR2,
                       'LDR3' : pca9632_constant.LDR3 }
                       
   ledout_mode = { 'OFF' : pca9632_constant.OFF,
                   'ON'  : pca9632_constant.ON,
                   'PWM' : pca9632_constant.PWM,
                   'PWM_GRPPWM' : pca9632_constant.PWM_GRPPWM }
                   
   ldr0 = PCA9632().read_register( register = 'LEDOUT' ) & 0x03 
   ldr1 = (PCA9632().read_register( register = 'LEDOUT' ) & 0x0c) >> 2
   ldr2 = (PCA9632().read_register( register = 'LEDOUT' ) & 0x30) >> 4
   ldr3 = (PCA9632().read_register( register = 'LEDOUT' ) & 0xc0) >> 6
   
   if (ldr0 == ledout_mode ['PWM'] or (ldr0 == ledout_mode ['PWM_GRPPWM'] and reg_mode2['DMBLNK'] == 'BLINKING')) : 
     register['PWM0'] = round(PCA9632().read_register( register = 'PWM0' ) / 256 * 100,1)
   elif ldr0 == ledout_mode ['PWM_GRPPWM'] :
     register['PWM0'] = round((PCA9632().read_register( register = 'PWM0' ) & 0xFC) / 256 * 100,1) 
   elif ldr0 == ledout_mode ['ON'] :
     register['PWM0'] = 100
   else:
     register['PWM0'] = 0
   if (ldr1 == ledout_mode ['PWM'] or (ldr1 == ledout_mode ['PWM_GRPPWM'] and reg_mode2['DMBLNK'] == 'BLINKING')) : 
     register['PWM1'] = round(PCA9632().read_register( register = 'PWM1' ) / 256 * 100,1)
   elif ldr1 == ledout_mode ['PWM_GRPPWM'] :
     register['PWM1'] = round((PCA9632().read_register( register = 'PWM1' ) & 0xFC) / 256 * 100,1) 
   elif ldr1 == ledout_mode ['ON'] :
     register['PWM1'] = 100
   else:
     register['PWM1'] = 0
   if (ldr2 == ledout_mode ['PWM'] or (ldr2 == ledout_mode ['PWM_GRPPWM'] and reg_mode2['DMBLNK'] == 'BLINKING')) : 
     register['PWM2'] = round(PCA9632().read_register( register = 'PWM2' ) / 256 * 100,1)
   elif ldr2 == ledout_mode ['PWM_GRPPWM'] :
     register['PWM2'] = round((PCA9632().read_register( register = 'PWM2' ) & 0xFC) / 256 * 100,1) 
   elif ldr2 == ledout_mode ['ON'] :
     register['PWM2'] = 100
   else:
     register['PWM2'] = 0
   if (ldr3 == ledout_mode ['PWM'] or (ldr3 == ledout_mode ['PWM_GRPPWM'] and reg_mode2['DMBLNK'] == 'BLINKING')) : 
     register['PWM3'] = round(PCA9632().read_register( register = 'PWM3' ) / 256 * 100,1)
   elif ldr3 == ledout_mode ['PWM_GRPPWM'] :
     register['PWM3'] = round((PCA9632().read_register( register = 'PWM3' ) & 0xFC) / 256 * 100,1) 
   elif ldr3 == ledout_mode ['ON'] :
     register['PWM3'] = 100
   else:
     register['PWM3'] = 0
   register['GRPPWM'] = str(PCA9632().read_register( register = 'GRPPWM' ))
   register['GRPFREQ'] = str(PCA9632().read_register( register = 'GRPFREQ' )) 
                   
   
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
      
      
   register['SUBADR1'] = str(hex((PCA9632().read_register( register = 'SUBADR1' ) & 0xFE) >> 1))
   register['SUBADR2'] = str(hex((PCA9632().read_register( register = 'SUBADR2' ) & 0xFE) >> 1))
   register['SUBADR3'] = str(hex((PCA9632().read_register( register = 'SUBADR3' ) & 0xFE) >> 1))
   
   register['LEDOUT'] = reg_ledout
   
   register['ALLCALLADR'] = str(hex((PCA9632().read_register( register = 'ALLCALLADR' ) & 0xFE) >> 1))
   
   return (register)
 
def software_reset (address=pca9632_constant.PCA9632_SWRESET, busnum=pca9632_constant.I2CBUS, i2c=None, **kwargs):
    '''Sends a software reset (SWRST) command to all servo drivers on the bus.'''
    # Setup I2C interface for device 0x00 to talk to all of them.

    if i2c is None:
        import ecomet_i2c_sensors.i2c as I2C
        i2c = I2C
    try:
      device = i2c.get_i2c_device(address, busnum, **kwargs) # SWRST
      device.writeRaw8(0xa5)
      device.writeRaw8(0x5a)
    except:
      return 1
    else:
      return 0
      
def ledout_clear ():
   try:
    PCA9632().write_register(register = 'LEDOUT', bits = [{'LDR0' : 'OFF'},{'LDR1' : 'OFF'},{'LDR2' : 'OFF'},{'LDR3' : 'OFF'}])
   except:
      return 1
   else:
      return 0

class PCA9632(object):
    '''PCA9632() PWM LED/servo controller.'''

    def __init__(self, address=pca9632_constant.PCA9632_ADDRESS, i2c=None, **kwargs) :
        '''Initialize the PCA9685.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        #self._device.write8(PWM0,0x7D)
    def self_test(self) :
        try :
          self.read_register( register = 'MODE1')
        except :
          return 1
        else :
          return 0
    def read_register(self, register) :
        return self._device.readU8(reg_list[register])
    def write_register(self, register, bits) :
          ret = 0
          reg_status = self.read_register( register = register )
          if register == 'MODE1' :
           for ibit in bits :
             try :
                bit = mode1_bit_on_list[ibit]
                reg_status = reg_status ^ bit
             except :
                bit = mode1_bit_off_list[ibit]
                reg_status = reg_status & bit
             finally:
                try :
                  self._device.write8(reg_list[register],int(reg_status))
                except :
                  ret = ret + 1
                else :
                  ret = ret + 0
          elif register == 'MODE2' :
           for ibit in bits :
             try :
                bit = mode2_bit_on_list[ibit] 
                reg_status = reg_status ^ bit
             except :
                bit = mode2_bit_off_list[ibit]
                reg_status = reg_status & bit
             finally:
                try :
                  self._device.write8(reg_list[register],int(reg_status))
                except :
                  ret = ret + 1
                else :
                  ret = ret + 0
          elif register == 'PWM0' :
           for key, value in bits[0].items() :
              if key == 'PWM' :
                 pass
              elif key == 'GRPPWM' :
                 value = int(value) & 0xFC
              try:
                 self._device.write8(reg_list[register],int(value))
              except :
                 ret = 1
              else :
                 ret = 0
          elif register == 'PWM1' :
           for key, value in bits[0].items() :
              if key == 'PWM' :
                 pass
              elif key == 'GRPPWM' :
                 value = int(value) & 0xFC
              try:
                 self._device.write8(reg_list[register],int(value))
              except :
                 ret = 1
              else :
                 ret = 0
          elif register == 'PWM2' :
           for key, value in bits[0].items() :
              if key == 'PWM' :
                 pass
              elif key == 'GRPPWM' :
                 value = int(value) & 0xFC
              try:
                 self._device.write8(reg_list[register],int(value))
              except :
                 ret = 1
              else :
                 ret = 0
          elif register == 'PWM3' :
           for key, value in bits[0].items() :
              if key == 'PWM' :
                 pass
              elif key == 'GRPPWM' :
                 value = int(value) & 0xFC
              try:
                 self._device.write8(reg_list[register],int(value))
              except :
                 ret = 1
              else :
                 ret = 0
          elif register == 'GRPPWM' :
            for key, value in bits[0].items() :
              try:
                 self._device.write8(reg_list[register],int(value))
              except :
                 ret = 1
              else :
                 ret = 0       
          elif register == 'GRPFREQ' :
            for key, value in bits[0].items() :
              try:
                 self._device.write8(reg_list[register],int(value))
              except :
                 ret = 1
              else :
                 ret = 0 
          elif register == 'LEDOUT' :
           for ibit in bits :
              bit_key = list(ibit)[0]
              bit_value = ibit[bit_key]
              self.set_def_LDRx( register = bit_key, mode = bit_value)
              index = bit_key[3:]
              bit_led = led_bit_mode[bit_value]
              bit_m1 = reg_status & led_bit_list[bit_key]
              bit_m1 = '00000000'[:(8 - len(bin(bit_m1)[2:]))] + bin(bit_m1)[2:]
              if index == '3' :
                 bit_m2 = '00'[:(2 - len(bin(bit_led)[2:]))] + bin(bit_led)[2:] + '000000'
              elif index == '2' :
                    bit_m2 = '0000'[:(2 - len(bin(bit_led)[2:]))] + bin(bit_led)[2:] + '0000'
              elif index == '1' :
                    bit_m2 = '000000'[:(2 - len(bin(bit_led)[2:]))] + bin(bit_led)[2:] + '00'
              else :
                    bit_m2 = '00000000'[:(8 - len(bin(bit_led)[2:]))] + bin(bit_led)[2:]
              try :
                reg_status = int(bit_m1,2) ^ int(bit_m2,2) 
                self._device.write8(reg_list[register],int(reg_status))
              except :
                 ret = ret + 1
              else :
                 ret = ret + 0
          return ret
    def set_def_LDRx(self, register, mode) :
          ret = 0
          if register == 'LDR0' :
             write_reg = 'PWM0'
          elif register == 'LDR1' :
             write_reg = 'PWM1'
          elif register == 'LDR2' :
             write_reg = 'PWM2'
          else :
             write_reg = 'PWM3'
          if mode == 'OFF' :
            set_value = 0x00
          elif mode == 'ON' :
            set_value = 0xFF
          try:
            self._device.write8(reg_list[write_reg],set_value)
          except :
                 ret = ret + 1
          else :
                 ret = ret + 0
          return ret
                
                      
