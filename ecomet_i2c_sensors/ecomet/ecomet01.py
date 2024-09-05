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

reg_list = { 'CONF0' : ecomet01_constant.CONF0, 'CONF1' :  ecomet01_constant.CONF1, 'CONF2' : ecomet01_constant.CONF2, 'CONF3' :  ecomet01_constant.CONF3,
             'READ0' : ecomet01_constant.READ0, 'READ1' :  ecomet01_constant.READ1, 'READ2' : ecomet01_constant.READ2, 'READ3' :  ecomet01_constant.READ3,
        }

class ECOMET01:

    def __init__(self,address=ecomet01_constant.ECOMET_ADDR, busnum=1, i2c=None, **kwargs):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)  
        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface='smbus2', **kwargs)

 #   @property
    def read_register(self, register) :
       #return self._device.readU8(0x51)
       return self._device.readU8(reg_list[register])
       #return self._device.readRaw8()
       #return self._device.readList(reg_list[register],2)

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

