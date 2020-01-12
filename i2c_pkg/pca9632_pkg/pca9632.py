from __future__ import division
import logging
import time
import math
import pca9632_constant
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
                
mode2_bit_on_list = { 'DMBLNK' : pca9632_constant.DMBLNK,
                      'INVRT' : pca9632_constant.INVRT,
                      'OCH' : pca9632_constant.OCH,
                      'OUTDRV' : pca9632_constant.OUTDRV
                }

mode2_bit_off_list = { 'DMBLNK_N' : pca9632_constant.DMBLNK_N,
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
 
def software_reset (i2c=None, **kwargs):
    '''Sends a software reset (SWRST) command to all servo drivers on the bus.'''
    # Setup I2C interface for device 0x00 to talk to all of them.

    if i2c is None:
        import Adafruit_GPIO.I2C as I2C
        i2c = I2C
    self._device = i2c.get_i2c_device(0x00, **kwargs)
    self._device.writeRaw8(pca9632_constant.PCA9632_SWRESET)  # SWRST
    self._device.writeRaw8(0xa5)
    self._device.writeRaw8(0x5a)
'''    
def read_subadr(register, address, suba=None, **kwargs) :
     sub_list = { 'SUBADR1' : SUBADR1_R,
                  'SUBADR2' : SUBADR2_R,
                  'SUBADR3' : SUBADR3_R 
                 }
     if suba is None:
         import Adafruit_GPIO.I2C as I2C
         suba = I2C
     _sub = suba.get_i2c_device(sub_list[register], **kwargs)
     return _sub.readU8(address)
'''

class PCA9632(object):
    '''PCA9632 PWM LED/servo controller.'''

    def __init__(self, address=pca9632_constant.PCA9632_ADDRESS, i2c=None, **kwargs) :
        '''Initialize the PCA9685.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        self._device.write8(pca9632_constant.LEDOUT,0x00)
        #self._device.write8(PWM0,0x7D)
    def read_register(self, register) :
        return self._device.readU8(reg_list[register])
    def write_register(self, register, bits) :
          reg_status = self.read_register( register = register )
          if register == 'MODE1' :
           for ibit in bits :
             try :
                bit = mode1_bit_on_list[ibit]
                reg_status = reg_status ^ bit
             except :
                bit = mode1_bit_off_list[ibit]
                reg_status = reg_status & bit
          elif register == 'MODE2' :
           for ibit in bits :
             try :
                bit = mode2_bit_on_list[ibit] 
                reg_status = reg_status ^ bit
             except :
                bit = mode2_bit_off_list[ibit]
                reg_status = reg_status & bit
          elif register == 'LEDOUT' :
           for ibit in bits :
              bit_key = list(ibit)[0]
              bit_value = ibit[bit_key]
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
                    
                  
              reg_status = int(bit_m1,2) ^ int(bit_m2,2)
          try :
           self._device.write8(reg_list[register],int(reg_status))
          except :
             return 1
          else :
             return 0
