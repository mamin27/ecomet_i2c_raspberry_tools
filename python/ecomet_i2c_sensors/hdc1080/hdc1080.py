from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.hdc1080 import hdc1080_constant
#import hdc1080_constant
#import i2c_command_oop

def power (base, exponent) :
   if exponent == 0 :
      return 1
   else :
      return base * power (base, exponent -1)

reg_list = { 'TEMP' : hdc1080_constant.TEMP, 'HUMDT' :  hdc1080_constant.HUMDT, 
             'CONF' : hdc1080_constant.CONF, 'SER_ID1' : hdc1080_constant.SER_ID1, 'SER_ID2' : hdc1080_constant.SER_ID2, 'SER_ID3' : hdc1080_constant.SER_ID3,
             'MANUF' : hdc1080_constant.MANUF, 'DEVID' : hdc1080_constant.DEVID,
        }
conf_bit_on_list = { 'HRES_RES1' : hdc1080_constant.HRES_RES1,
                     'HRES_RES2' : hdc1080_constant.HRES_RES2,
                     'HRES_RES3' : hdc1080_constant.HRES_RES3,
                     'TRES_RES1' : hdc1080_constant.TRES_RES1,
                     'TRES_RES2' : hdc1080_constant.TRES_RES2,
                     'BTST_HI' : hdc1080_constant.BTST_HI,
                     'BTST_LO' : hdc1080_constant.BTST_LO,
                     'MODE_ONLY' : hdc1080_constant.MODE_ONLY,
                     'MODE_BOTH' : hdc1080_constant.MODE_BOTH,
                     'HEAT_DISABLE' : hdc1080_constant.HEAT_DISABLE,
                     'HEAT_ENABLE' : hdc1080_constant.HEAT_ENABLE,
                     'RST_ON' : hdc1080_constant.RST_ON
                }

conf_bit_off_list = { 'HRES_RES1_CLR' : hdc1080_constant.HRES_RES1_CLR,
                      'HRES_RES2_CLR' : hdc1080_constant.HRES_RES2_CLR,
                      'HRES_RES3_CLR' : hdc1080_constant.HRES_RES3_CLR,
                      'TRES_RES1_CLR' : hdc1080_constant.TRES_RES1_CLR,
                      'TRES_RES2_CLR' : hdc1080_constant.TRES_RES2_CLR,
                      'BTST_HI_CLR' : hdc1080_constant.BTST_HI_CLR,
                      'BTST_LO_CLR' : hdc1080_constant.BTST_LO_CLR,
                      'MODE_ONLY_CLR' : hdc1080_constant.MODE_ONLY_CLR,
                      'MODE_BOTH_CLR' : hdc1080_constant.MODE_BOTH_CLR,
                      'HEAT_DISABLE_CLR' : hdc1080_constant.HEAT_DISABLE_CLR,
                      'HEAT_ENABLE_CLR' : hdc1080_constant.HEAT_ENABLE_CLR,
                      'RST_ON_CLR' : hdc1080_constant.RST_ON_CLR
                }
   
conf_mask_bit_list = { 'CONF_HRES' : hdc1080_constant.CONF_HRES,
                       'CONF_TRES' : hdc1080_constant.CONF_TRES,
                       'CONF_BAT' : hdc1080_constant.CONF_BAT,
                       'CONF_MODE' : hdc1080_constant.CONF_MODE,
                       'CONF_HEAT' : hdc1080_constant.CONF_HEAT
                      }
                      
logger = logging.getLogger(__name__) 

def register_list() :

   hdc = HDC1080()
   hdc._logger = logging.getLogger('ecomet.hdc1080.reglist') 
   register = {}
   
   reg_conf = {}
   reg_id = {}
   
   hres_switch = { 0: '14BIT',
                   256: '11BIT',
                   512: '8BIT' }
   
   tres_switch = { 0: '14BIT',
                   1024: '11BIT' }
                   
   reg_conf['HRES'] = hres_switch.get((hdc.read_register( register = 'CONF' )[0] & conf_mask_bit_list['CONF_HRES']))
   reg_conf['TRES'] = tres_switch.get((hdc.read_register( register = 'CONF' )[0] & conf_mask_bit_list['CONF_TRES']))
   reg_conf['BAT'] = 'LOW' if hdc.read_register( register = 'CONF' )[0] & conf_mask_bit_list['CONF_BAT'] > 0 else 'GOOD'      
   reg_conf['MODE'] = 'BOTH' if hdc.read_register( register = 'CONF' )[0] & conf_mask_bit_list['CONF_MODE'] > 0 else 'ONLY'      
   reg_conf['HEAT'] = 'ENABLE' if hdc.read_register( register = 'CONF' )[0] & conf_mask_bit_list['CONF_HEAT'] > 0 else 'DISABLE' 
        
   reg_id['SERIAL'] = hdc.serial()[0]
   reg_id['MANUF'] = hdc.manufacturer()[0]
   reg_id['DEVID'] = hdc.deviceid()[0]
   
   register['CONF'] = reg_conf
   register['ID'] = reg_id
   
   return (register);
   
def measure_list() :
   
   hdc = HDC1080()
   hdc._logger = logging.getLogger('ecomet.hdc1080.reglist') 
   measure = {}
   mlist = {}
   ret = 0
   
   if hdc.read_register( register = 'CONF' )[0] & conf_mask_bit_list['CONF_MODE'] > 0 : 
     (mlist['TEMP'],mlist['HMDT'],ret) = hdc.both_measurement()
   else :
     (mlist['TEMP'],nret) = hdc.measure_temp()
     ret = ret + nret
     (mlist['HMDT'],nret) = hdc.measure_hmdt()
     ret = ret + nret
     
   measure['MEASURE'] = mlist
   
   return (measure,ret)

class HDC1080(object):
    '''HDC1080() PWM LED/servo controller.'''

    def __init__(self, address=hdc1080_constant.HDC1080_ADDRESS, busnum=hdc1080_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the HDC1080.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
    def self_test(self) :
        try :
          ret = self.battery()
        except :
          ret = 1
        return ret
    def read_register(self, register) :
        if register == 'TEMP' or register == 'HUMDT' or register == 'CONF' or register == 'SER_ID1' or register == 'SER_ID2' or register == 'SER_ID3' or register == 'MANUF' or register == 'DEVID' :
           ret = 0
           try:
              reg_status_bita = self._device.readList(reg_list[register],2)
              if not reg_status_bita:
                return (0x0000,2)
              reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0]) + '{0:02x}'.format(reg_status_bita[1])
              reg_status = int(reg_status_hex, 0)
           except :
              ret = ret + 1;
           if ret > 1 :
              self._logger.debug('read_register %s failed (%s)',register,ret)
              return (0x0000,ret)
           else :
              self._logger.debug('read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
              self._logger.debug('read_register %s, data: %s', register, '{0:b}'.format(reg_status))
              return (reg_status,0)
    def write_register(self, register, bits) :
          ret = 0
          (reg_status,ret) = self.read_register( register = register )
          if register == 'CONF' :
           for ibit in bits :
               #bit = conf_bit_on_list[ibit]
               bit_clr = ibit + '_CLR'
               reg_status = reg_status & conf_bit_off_list[bit_clr]
               self._logger.debug('write_register, init reg_status: %s, bit_mask_reg %s', '{0:04X}'.format(reg_status), format(bit_clr))
               reg_status = reg_status | conf_bit_on_list[ibit]
               self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:04X}'.format(reg_status), '{0:04X}'.format(conf_bit_on_list[ibit]))
           reg_status_msb = (reg_status >> 8) & 0xff
           reg_status_lsb = reg_status & 0xff
           reg_status_msb = reg_status_msb.to_bytes(length=1, byteorder='big')
           reg_status_lsb = reg_status_lsb.to_bytes(length=1, byteorder='big')
           byt_reg = bytearray()
           byt_reg += bytearray(reg_status_msb)
           byt_reg += bytearray(reg_status_lsb)
           try :
               self._device.writeList(reg_list[register],byt_reg);
           except :
               ret = ret + 1
               self._logger.debug('writelist error')
          else :
              ret = 1
          if ret > 1 :
             self._logger.debug('write_register %s failed (%s)', register, ret)
          else :
             self._logger.debug('write_register %s, byte data: %s', register,byt_reg)
             self._logger.debug('write_register %s, data: %s', register, '{0:04X}'.format(reg_status))
          return ret
    def write_mert_invoke (self, register) :
        if register == 'TEMP' or register == 'HUMDT' :
            try :
                self._device.writeRaw8(reg_list[register]);
            except :
                self._logger.info('write_invoke %s mask failed', register)
                return 1
            finally :
                self._logger.info('write_invoke %s mask', register)
                return 0
    def both_measurement (self) :
        byt_reg = ()
        ret = 0
        ret = self.write_register( register = 'CONF', bits = ['MODE_BOTH'])
        from time import sleep
        ret = ret + self.write_mert_invoke( register = 'TEMP' )
        sleep(0.02)
        byt_reg = self._device.readRaw32()
        self._logger.debug('temp byte: %s', hex(byt_reg[1] + (byt_reg[0] << 8)))
        self._logger.debug('humdt byte: %s', hex(byt_reg[3] + (byt_reg[2] << 8)))
        temp = int(byt_reg[1] + (byt_reg[0] << 8))
        temp = temp/power(2,16)
        temp = temp*165 - 40
        humdt = int(byt_reg[3] + (byt_reg[2] << 8))
        humdt = humdt/power(2,16)
        humdt = humdt*100
        return  (temp, humdt, ret)
    def measure_temp (self) :
        byt_reg = ()
        ret = 0
        ret = self.write_register( register = 'CONF', bits = ['MODE_ONLY'])
        from time import sleep
        ret = ret + self.write_mert_invoke( register = 'TEMP')
        sleep(0.01)
        byt_reg = self._device.readRaw16()
        self._logger.debug('temp byte: %s', hex(byt_reg[1] + (byt_reg[0] << 8)))
        temp = int(byt_reg[1] + (byt_reg[0] << 8))
        temp = temp/power(2,16)
        temp = temp*165 - 40
        return (temp,ret)
    def measure_hmdt (self) :
        byt_reg = ()
        ret = 0
        ret = self.write_register( register = 'CONF', bits = ['MODE_ONLY'])
        from time import sleep
        ret = ret + self.write_mert_invoke( register = 'HUMDT')
        sleep(0.01)
        byt_reg = self._device.readRaw16()
        self._logger.debug('temp byte: %s', hex(byt_reg[1] + (byt_reg[0] << 8)))
        hmdt = int(byt_reg[1] + (byt_reg[0] << 8))
        hmdt = hmdt/power(2,16)
        hmdt = hmdt*100
        return (hmdt,ret)
    def sw_reset (self) :
        ret = self.write_register( register = 'CONF', bits = ['RST_ON'])
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def battery (self) :
        (reg_status,ret) = self.read_register( register = 'CONF' )
        reg_status = reg_status & conf_bit_on_list['BTST_LO']
        if reg_status > 0 :
            ret = 1
        else :
            ret = 0
        return ret
    def serial (self) :
       ret = 0
       (byte1,lret) = self.read_register( register = 'SER_ID1' )
       if lret > 0 :
          ret = ret + 1
       (byte2,lret) = self.read_register( register = 'SER_ID2' )
       if lret > 0 :
          ret = ret + 1
       (byte3,lret) = self.read_register( register = 'SER_ID3' )
       if lret > 0 :
          ret = ret + 1
       if ret > 0 : 
           self._logger.error('Read error %s'.format(ret))
           return (0,ret)
       else :
           self._logger.debug('Serial: %s:%s:%s','{0:04X}'.format(byte1),'{0:04X}'.format(byte2),'{0:04X}'.format(byte3))
           return ('{0:04X}'.format(byte1) + '-' + '{0:04X}'.format(byte2) + '-' + '{0:04X}'.format(byte3),0)
    def manufacturer (self) :
       ret = 0
       (temp,lret) = self.read_register( register = 'MANUF' )
       if lret > 0 :
          ret = ret + 1
       if ret > 0 : 
           self._logger.error('Read error %s'.format(ret))
           return (0,ret)
       else :
           self._logger.debug('Serial: %s','{0:04X}'.format(temp))
           return ('{0:04X}'.format(temp),0)
    def deviceid (self) :
       ret = 0
       (temp,lret) = self.read_register( register = 'DEVID' )
       if lret > 0 :
          ret = ret + 1
       if ret > 0 : 
           self._logger.error('Read error %s'.format(ret))
           return (0,ret)
       else :
           self._logger.debug('DeviceID: %s','{0:04X}'.format(temp))
           return ('{0:04X}'.format(temp),0)
