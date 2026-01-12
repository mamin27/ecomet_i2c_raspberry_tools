''' 
  Updated Code: 2024-07-11
  Copyright (c) 2024 eComet Co.Ltd (https://twitter.com/mminar7)
  @author      <mminar7@gmail.com>
  @license	   GPL-3.0
'''

from time import sleep, time
import smbus2
import logging
from ecomet import ecomet01_constant

reg_list = { 'REG00' : ecomet01_constant.REG00,
             'REG01' : ecomet01_constant.REG01, 'REG02' :  ecomet01_constant.REG02, 'REG03' : ecomet01_constant.REG03,
             'REG04' : ecomet01_constant.REG04, 'REG05' :  ecomet01_constant.REG05,
        }

class ECOMET01:

    def __init__(self,address=ecomet01_constant.ECOMET_ADDR, busnum=1, i2c=None, **kwargs):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)  
        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface=None, **kwargs)

    @property
    def read_value(self) :
       ret = 0
       try :
          reg_status = self._device.readRaw16()
          decimal_number = (reg_status[0] << 8) | reg_status[1]
          self._logger.debug('Dec_Num: %s',decimal_number)
          out = decimal_number/mcp3221_constant.MAX_VDD
          self._logger.debug('Number: %s',out)
       except :
             ret = ret + 1
       return(out,ret)

#    @property
    def read_register(self, register = None):
       if register == 'REG01' or register == 'REG02' or register == 'REG03' or register == 'REG04' or register == 'REG05' or register == 'REG00' or register == 'REG06' \
          or register == 'REG_UNI':
           ret = 0
           if register == 'REG00' or register == 'REG01' or register == 'REG02':
               try:
                   reg_status_bita = self._device.readList(reg_list[register],1)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           elif register == 'REG03':
               try:
                   reg_status_bita = self._device.readList(reg_list[register],2)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           elif register == 'REG_UNI':
               try:
                   reg_status_bita = self._device.readRawBytes(9)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
               self._logger.debug('read data: 0x%s[0b%s]','{0:04X}'.format(reg_status), '{0:16b}'.format(reg_status))
               return (reg_status,0)
           elif register == 'REG04':
               try:
                   reg_status_bita = self._device.readList(reg_list[register],4)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           if ret > 1 :
              self._logger.debug('read_register %s failed (%s)',register,ret)
              return (0x0000,ret)
           else :
              self._logger.debug('read_register %s, data: 0x%s[0b%s]', register,'{0:04X}'.format(reg_status), '{0:16b}'.format(reg_status))
              return (reg_status,0)

    def write_register(self, register = None, value = []):
       if register == 'REG00' or register == 'REG01' or register == 'REG02' \
          or register == 'REG03' or register == 'REG04' or register == 'REG05':
           ret = 0
           if register == 'REG00' or register == 'REG01' or register == 'REG02' \
           or register == 'REG03' or register == 'REG04' or register == 'REG05':
               try:
                   self._device.writeList(register = reg_list[register], data = value)
               except:
                   ret = ret + 1
           if ret > 1 :
              self._logger.debug('write_register %s failed (%s)',register,ret)
              return (ret)
           else :
              self._logger.debug('write_register %s, data [%s]', register, format(':'.join(hex(x) for x in value)))
              return (ret)

