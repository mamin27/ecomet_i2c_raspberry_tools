''' 
  Updated Code: 2024-07-11
  Copyright (c) 2024 eComet Co.Ltd (https://twitter.com/mminar7)
  @author      <mminar7@gmail.com>
  @license	   GPL-3.0
'''
from __future__ import division
from time import sleep, time
import logging
from ecomet_i2c_sensors.i2c import load_comet_yaml
from ecomet_i2c_sensors.ecomet.winds01 import winds01_constant

reg_list = { 'REG_SERIAL_NUMBER' : winds01_constant.REG_SERIAL_NUMBER,
             'REG_CONF' : winds01_constant.REG_CONF, 'REG_INIT' :  winds01_constant.REG_INIT, 
             'REG_ValidCnt' : winds01_constant.REG_ValidCnt, 'REG_EE_Index': winds01_constant.REG_EE_Index,
             'REG_TACH_TIC_Cnt' : winds01_constant.REG_TACH_TIC_Cnt,
             'REG_AVG00' : winds01_constant.REG_AVG00, 'REG_AVG30' : winds01_constant.REG_AVG30,
             'REG_AVG60' : winds01_constant.REG_AVG60, 'REG_AVG360' : winds01_constant.REG_AVG360,
             'REG_GUST00' : winds01_constant.REG_GUST00, 'REG_GUST30' : winds01_constant.REG_GUST30,
             'REG_GUST60' : winds01_constant.REG_GUST60, 'REG_GUST360' : winds01_constant.REG_GUST360,
             'REG_BULK': winds01_constant.REG_BULK, 'REG_EEPROM_AVG' : winds01_constant.REG_EEPROM_AVG, 'REG_EEPROM_GUST' : winds01_constant.REG_EEPROM_GUST
             
        }

class WINDS01:

    def __init__(self,address=winds01_constant.WINDS_ADDR, busnum=None, i2c=None, **kwargs):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)  
        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface=None, **kwargs)
        smb = load_comet_yaml()
        if smb != -99 :
           busnum = smb['i2c']['smb'].replace('i2c-', '')
           print (f"busnum: {busnum}")
        else :
           busnum = 0

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
       if register == 'REG_SERIAL_NUMBER' or register == 'REG_CONF' or register == 'REG_INIT' or register == 'REG_ValidCnt' or register == 'REG_EE_Index' or register == 'REG_TACH_TIC_Cnt' \
          or register == 'REG_AVG00' or register == 'REG_AVG30' or register == 'REG_AVG60' or register == 'REG_AVG360' \
          or register == 'REG_GUST00' or register == 'REG_GUST30' or register == 'REG_GUST60' or register == 'REG_GUST360' \
          or register == 'REG_BULK' or register == 'REG_EEPROM_AVG' or register == 'REG_EEPROM_GUST':
           ret = 0
           if register == 'REG_CONF' or register == 'REG_INIT' or register == 'REG_ValidCnt' or register == 'REG_EE_Index' or register == 'REG_TACH_TIC_Cnt' :
               try:
                   reg_status_bita = self._device.readList(reg_list[register],1)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           elif register == 'REG_AVG00' or register == 'REG_GUST00' or register == 'REG_GUST30' or register == 'REG_GUST60' or register == 'REG_GUST360':
                   try:
                       reg_status_bita = self._device.readList(reg_list[register],2)
                       reg_status = int.from_bytes(reg_status_bita,byteorder='big')
                   except:
                       ret = ret + 1
           elif register == 'REG_AVG30' or register == 'REG_AVG60' or register == 'REG_AVG360' :
                   try:
                       reg_status_bita = self._device.readList(reg_list[register],3)
                       reg_status = int.from_bytes(reg_status_bita,byteorder='big')
                   except:
                       ret = ret + 1
           elif register == 'REG_SERIAL_NUMBER':
               try:
                   reg_status_bita = self._device.readList(reg_list[register],4)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           elif register == 'REG_EEPROM_AVG' or register == 'REG_EEPROM_GUST':
               try:
                   reg_status_bita = self._device.readList(reg_list[register],128)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           elif register == 'REG_BULK':
               try:
                   reg_status_bita = self._device.readList(reg_list[register],21)
                   reg_status = int.from_bytes(reg_status_bita,byteorder='big')
               except:
                   ret = ret + 1
           if ret > 1 :
              self._logger.debug('read_register %s failed (%s)',register,ret)
              return (0x0000,ret)
           elif ret == 0 and (register == 'REG_ValidCnt' or register == 'REG_EE_Index'):
              self._logger.debug('read_register %s, data: 0x%s[0b%s]', register,'{0:02X}'.format(reg_status), '{0:8b}'.format(reg_status))
              return (reg_status,0)
           elif ret == 0 and (register == 'REG_CONF' or register == 'REG_INIT'):
              self._logger.debug('read_register %s, data: 0x%s[0b%s]', register,'{0:02X}'.format(reg_status), '{0:8b}'.format(reg_status))
              return (reg_status,0)
           elif ret == 0 and (register == 'REG_AVG00' or register == 'REG_GUST00' or register == 'REG_GUST30' or register == 'REG_GUST60' or register == 'REG_GUST360'):
              self._logger.debug('read_register %s, data: 0x%s[0b%s]', register,'{0:04X}'.format(reg_status), '{0:16b}'.format(reg_status))
              return (reg_status,0)
           elif ret == 0 and (register == 'REG_AVG30' or register == 'REG_AVG60' or register == 'REG_AVG360'):
              self._logger.debug('read_register %s, data: 0x%s[0b%s]', register,'{0:06X}'.format(reg_status), '{0:24b}'.format(reg_status))
              return (reg_status,0)
           elif ret == 0 and (register == 'REG_EEPROM_AVG' or register == 'REG_EEPROM_GUST' or register == 'REG_BULK'):
              self._logger.debug('read_register %s, data: 0x%s', register, ''.join(f'{b:02X}' for b in reg_status)
                 if isinstance(reg_status, (bytes, bytearray, list, tuple))
                 else f'{reg_status:X}'.zfill(8)          # ← 8 = 32-bit, change to 4 if 16-bit
              )
              return (reg_status,0)
           else :
              self._logger.debug('read_register %s, data: 0x%s', register,'{0:04X}'.format(reg_status))
              return (reg_status,0)

    def write_register(self, register = None, value = []):
       if register == 'REG_CONF' or register == 'REG_INIT' or register == 'REG_TACH_TIC_Cnt':
           ret = 0
           if register == 'REG_CONF' or register == 'REG_INIT' or register == 'REG_TACH_TIC_Cnt':
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

