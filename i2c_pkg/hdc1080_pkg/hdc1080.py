from __future__ import division
import logging
import time
import math
from i2c_pkg.hdc1080_pkg import hdc1080_constant
#import hdc1080_constant
#import i2c_command_oop

reg_list = { 'TEMP' : hdc1080_constant.TEMP, 'HUMDT' :  hdc1080_constant.HUMDT, 
             'CONF' : hdc1080_constant.CONF, 'SER_ID1' : hdc1080_constant.SER_ID1, 'SER_ID2' : hdc1080_constant.SER_ID2, 'SER_ID3' : hdc1080_constant.SER_ID3,
             'MANFU' : hdc1080_constant.MANFU, 'DEVID' : hdc1080_constant.DEVID,
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
                      'BTST_CLR' : hdc1080_constant.BTST_CLR,
                      'MODE_ONLY_CLR' : hdc1080_constant.MODE_ONLY_CLR,
                      'MODE_BOTH_CLR' : hdc1080_constant.MODE_BOTH_CLR,
                      'HEAT_DISABLE_CLR' : hdc1080_constant.HEAT_DISABLE_CLR,
                      'HEAT_ENABLE_CLR' : hdc1080_constant.HEAT_ENABLE_CLR,
                      'RST_ON_CLR' : hdc1080_constant.RST_ON_CLR
                }
                
mask_bit_list = { 'TEMP_BIT' : hdc1080_constant.TEMP_BIT,
                  'HUMDT_BIT' : hdc1080_constant.HUMDT_BIT,
                  'SER_ID1_BIT' : hdc1080_constant.SER_ID1_BIT,
                  'SER_ID2_BIT' : hdc1080_constant.SER_ID2_BIT,
                  'SER_ID3_BIT' : hdc1080_constant.SER_ID3_BIT,
                  'MAN1_BIT' : hdc1080_constant.MAN1_BIT,
                  'MAN2_BIT' : hdc1080_constant.MAN2_BIT
                }

logger = logging.getLogger(__name__) 

class HDC1080(object):
    '''HDC1080() PWM LED/servo controller.'''

    def __init__(self, address=hdc1080_constant.HDC1080_ADDRESS, i2c=None, **kwargs) :
        '''Initialize the HDC1080.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
    def read_register(self, register) :
        if register == 'TEMP' or register == 'HUMDT' or register == 'CONF' or register == 'SER_ID1' or register == 'SER_ID2' or register == 'SER_ID3' or register == 'MANFU' or register == 'DEVID' :
           ret = 0
           try:
              reg_status_bita = self._device.readList(reg_list[register],2)
              reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0]) + '{0:02x}'.format(reg_status_bita[1]);
              reg_status = int(reg_status_hex, 0)
           except :
              ret = ret + 1;
           if ret > 1 :
              self._logger.debug('read_register %s failed (%s)',register,ret)
              return (0x0000,ret)
           else :
              self._logger.debug('read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
              self._logger.debug('read_register %s, data: %s', register, '{0:b}'.format(reg_status));
              return (reg_status,0)
    def write_register(self, register, bits) :
          ret = 0
          (reg_status,ret) = self.read_register( register = register )
          if register == 'CONF' :
           for ibit in bits :
             try :
                bit = conf_bit_on_list[ibit]
                reg_status = reg_status ^ bit
                self._logger.debug('write_register, init reg_status: %s', '{0:04X}'.format(reg_status))
             except :
                bit = conf_bit_off_list[ibit]
                reg_status_msb = reg_status_msb & bit
                reg_status_lsb = 0
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
          elif register == 'TEMP' or register == 'HUMDT':
           for ibit in bits :
                bit = mask_bit_list[ibit] 
                reg_status = reg_status & bit
                try :
                  self._device.write16(reg_list[register],int(reg_status))
                except :
                  ret = ret + 1
          if ret > 1 :
             self._logger.debug('write_register %s failed (%s)', register, ret)
          else :
             self._logger.debug('write_register %s, byte data: %s', register,byt_reg)
             #self._logger.debug('write_register %s, data: %s', register, '{0:04X}'.format(reg_status))
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
           return ('{0:04X}'.format(byte1) + ':' + '{0:04X}'.format(byte2) + ':' + '{0:04X}'.format(byte3),0)
    def manufacturer (self) :
       ret = 0
       (temp,lret) = self.read_register( register = 'MANFU' )
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
'''           
    def sw_reset (self) :
          #   reg_status = self.read_register( register = 'CONF' )
          #   bit = conf_bit_on_list['RST_ON']
          #   reg_status = reg_status ^ bit
             try :
               self._device.write16(reg_list['CONF'],int(reg_status))
             except :
                ret = 1
             else :
                ret = 0
          return ret          
    def battery (self) :
        reg_status = self.read_register( register = 'CONF' )
        print ("{}".format(reg_status));
        #bit = conf_bit_off_list['BTST_CLR']
        #reg_status = reg_status & bit
        #try :
        #    bat_stat = self._device.readU16BE(reg_list[register] & bit)
        #except :
        #    ret = 10
        #    return ret
        #else :
        #    ret = bat_stat
        return 1'''
