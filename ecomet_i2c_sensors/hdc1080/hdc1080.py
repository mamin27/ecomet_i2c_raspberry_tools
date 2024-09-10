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
             'CONF' : hdc1080_constant.CONF, 'SER_ID1' : hdc1080_constant.SER_ID1,
             'SER_ID2' : hdc1080_constant.SER_ID2, 'SER_ID3' : hdc1080_constant.SER_ID3,
             'MANUF' : hdc1080_constant.MANUF, 'DEVID' : hdc1080_constant.DEVID,
           }
conf_bit = { 'HRES' : hdc1080_constant.HRES,
             'TRES' : hdc1080_constant.TRES,
             'BTST' : hdc1080_constant.BTST,
             'MODE' : hdc1080_constant.MODE,
             'HEAT' : hdc1080_constant.HEAT,
             'RST'  : hdc1080_constant.RST
            }

conf_stat = {'MODE_BOTH' : hdc1080_constant.MODE_BOTH,
             'MODE_ONLY' : hdc1080_constant.MODE_ONLY,
             'HRES_14'   : hdc1080_constant.HRES_14,
             'HRES_11'   : hdc1080_constant.HRES_11,
             'HRES_08'   : hdc1080_constant.HRES_08,
             'TRES_14'   : hdc1080_constant.TRES_14,
             'TRES_11'   : hdc1080_constant.TRES_11,
             'HEAT_DISABLE' : hdc1080_constant.HEAT_DISABLE,
             'HEAT_ENABLE'  : hdc1080_constant.HEAT_ENABLE,
             'RST_ON'    : hdc1080_constant.RST_ON
            }

conf_mask = {'MODE_Mask' : hdc1080_constant.MODE_Mask,
             'HRES_Mask' : hdc1080_constant.HRES_Mask,
             'TRES_Mask' : hdc1080_constant.TRES_Mask,
             'HEAT_Mask' : hdc1080_constant.HEAT_Mask,
             'BTST_Mask' : hdc1080_constant.BTST_Mask
             }

logger = logging.getLogger(__name__) 

def register_list() :

   hdc = HDC1080()
   hdc._logger = logging.getLogger('ecomet.hdc1080.reglist') 
   register = {}
   
   reg_conf = {}
   reg_id = {}
   
   hres_switch = { 0: '14BIT',
                   1: '11BIT',
                   3: '8BIT' }

   tres_switch = { 0: '14BIT',
                   1: '11BIT' }

   keys = hdc.read_register( register = 'CONF', bits = [{'HRES':'Mask'},{'TRES':'Mask'},{'BTST':'Mask'},{'MODE':'Mask'},{'HEAT':'Mask'}])
   reg_conf['HRES'] = hres_switch.get(keys[0]['HRES'])
   reg_conf['TRES'] = tres_switch.get(keys[0]['TRES'])
   reg_conf['BAT'] = 'LOW' if keys[0]['BTST'] > 0 else 'GOOD'
   reg_conf['MODE'] = 'BOTH' if keys[0]['MODE'] > 0 else 'ONLY'
   reg_conf['HEAT'] = 'ENABLE' if keys[0]['HEAT'] > 0 else 'DISABLE'

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

   keys = hdc.read_register( register = 'CONF', bits = [{'MODE':'Mask'}])
   if keys[0]['MODE'] > 0 :
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

    def __init__(self, address=hdc1080_constant.HDC1080_ADDRESS, busnum=None, i2c=None, **kwargs) :
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
    def read_register(self, register, bits = None) :
        if register == 'TEMP' or register == 'HUMDT' or register == 'CONF' or register == 'SER_ID1' or register == 'SER_ID2' or register == 'SER_ID3' or register == 'MANUF' or register == 'DEVID' :
           ret = 0
           try:
               reg_status_bita = self._device.readList(reg_list[register],2)
               reg_status = int.from_bytes(reg_status_bita,byteorder='big')
           except:
               ret = ret + 1
           if (register == 'CONF') & (bits != None):
               stat_bits = {}
               for ibit in bits :
                   if isinstance(ibit,dict):
                       keys = list(ibit.keys())
                       dvalue = keys[0]+'_Mask'
                       stat_bit = (reg_status & (conf_mask[dvalue] << conf_bit[keys[0]])) >>  conf_bit[keys[0]]
                       self._logger.debug('read_register: %s[%s] = %s', register, keys[0], '{0:4b}'.format(stat_bit))
                       stat_bits[keys[0]] = stat_bit
               return (stat_bits,0)
           if ret > 1 :
              self._logger.debug('read_register %s failed (%s)',register,ret)
              return (0x0000,ret)
           else :
              self._logger.debug('read_register %s, data: 0x%s[0b%s]', register,'{0:04X}'.format(reg_status), '{0:16b}'.format(reg_status))
              return (reg_status,0)
    def write_register(self, register, bits = None) :
        ret = 0
        (reg_status,ret) = self.read_register( register = register )
        if register == 'CONF' :
           for ibit in bits :
               if isinstance(ibit,dict):
                   keys = list(ibit.keys())
                   values = list(ibit.values())
                   dvalue = keys[0]+'_'+values[0]
                   if dvalue == 'MODE_BOTH':
                       reg_status = reg_status & 0b1110111111111111
                   else:
                       reg_status = reg_status | (conf_stat[dvalue] << conf_bit[keys[0]])
                   self._logger.debug('write_register preparation, init reg_status: %s[%s], bit %s', '{0:04x}'.format(reg_status), '{0:16b}'.format(reg_status), '{}'.format(keys[0]))
           try :
               self._device.writeList(reg_list[register],reg_status.to_bytes(2,byteorder='big'))
           except :
               ret = ret + 1
               self._logger.debug('write16 error')
        else :
           ret = 1
        if ret > 1 :
           self._logger.debug('write_register %s failed (%s)', register, ret)
        else :
           self._logger.debug('write_register %s, data: 0x%s, bits: 0b%s', register, '{0:04X}'.format(reg_status),'{0:16b}'.format(reg_status))
        return ret
    def write_mert_invoke (self, register) :
        if register == 'TEMP' or register == 'HUMDT' :
            try :
                self._device.writeRaw8(reg_list[register]);
            except :
                self._logger.debug('write_invoke %s mask failed', register)
                return 1
            finally :
                self._logger.debug('write_invoke %s mask', register)
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
        ret = self.write_register( register = 'CONF', bits = [{'RST':'ON'}])
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def battery (self) :
        (reg_status,ret) = self.read_register( register = 'CONF', bits = [{'BTST':'Mask'}])
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
