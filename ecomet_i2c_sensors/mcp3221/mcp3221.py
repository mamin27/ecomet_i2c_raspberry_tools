''' 
  Updated Code: 2024-07-11
  Copyright (c) 2024 eComet Co.Ltd (https://twitter.com/mminar7)
  @author      <mminar7@gmail.com>
  @license	   GPL-3.0
'''

from time import sleep, time
import smbus2
import logging
from ecomet_i2c_sensors.mcp3221 import mcp3221_constant

class MCP3221:

    def __init__(self,bus = 1,address=mcp3221_constant.MCP_ADDR, busnum=None, i2c=None, **kwargs):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)  
        self._device = i2c.get_i2c_device(address, busnum=busnum, **kwargs)

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

    @property
    def to_max_const(self) :
       ret = 0
       val = self.read_value
       if val[1] == 0 :
         out = val[0] * mcp3221_constant.MAX_DEGREE
       else :
         ret = ret + 1
       return (out,ret)

    '''
      @Convert degrees to cardinal points.
      @param degrees: Degrees (0-360)
      @return: Cardinal direction as a string
    '''
    @property
    def degrees_to_cardinal(self):
       ret = 0
       try :
          val = self.to_max_const
          degrees = val[0]
          if val[1] == 0  and (0 <= degrees < 360.1) :
             if (degrees >= 337.5 and degrees < 360.1) or (degrees >= 0 and degrees < 22.5):
                val = "North"
             elif degrees >= 22.5 and degrees < 67.5:
                val = "North-West"
             elif degrees >= 67.5 and degrees < 112.5:
                val = "West"
             elif degrees >= 112.5 and degrees < 157.5:
                val = "South-West"
             elif degrees >= 157.5 and degrees < 202.5:
                val = "South"
             elif degrees >= 202.5 and degrees < 247.5:
                val = "South-East"
             elif degrees >= 247.5 and degrees < 292.5:
                val = "East"
             elif degrees >= 292.5 and degrees < 337.5:
                val =  "North-East"
          else :
             val = "Error"
             ret = ret + 2
       except :
          ret = ret + 1
       return (val,ret)

    @property
    def degrees_to_cardinal_calibrated(self):
       ret = 0
       try :
          val = self.to_max_const
          degrees = val[0]
          if val[1] == 0  and (0 <= degrees < 360.1) :
             thr_n = ( mcp3221_constant.NORTH_WEST)/2
             thr_nw = mcp3221_constant.NORTH_WEST + ( mcp3221_constant.WEST - mcp3221_constant.NORTH_WEST )/2
             thr_w = mcp3221_constant.WEST + ( mcp3221_constant.SOUTH_WEST - mcp3221_constant.WEST )/2
             thr_sw = mcp3221_constant.SOUTH_WEST + ( mcp3221_constant.SOUTH - mcp3221_constant.SOUTH_WEST )/2
             thr_s = mcp3221_constant.SOUTH + ( mcp3221_constant.SOUTH_EAST - mcp3221_constant.SOUTH )/2
             thr_se = mcp3221_constant.SOUTH_EAST + ( mcp3221_constant.EAST - mcp3221_constant.SOUTH_EAST )/2
             thr_e = mcp3221_constant.EAST + ( mcp3221_constant.NORTH_EAST - mcp3221_constant.EAST )/2
             thr_ne = mcp3221_constant.NORTH_EAST + ( mcp3221_constant.NORTH - mcp3221_constant.NORTH_EAST )/2
             if (degrees >= thr_ne and degrees < 360.1) or (degrees >= 0 and degrees < thr_n):
                val = "North"
             elif degrees >= thr_n and degrees < thr_nw:
                val = "North-West"
             elif degrees >= thr_nw and degrees < thr_w:
                val = "West"
             elif degrees >= thr_w and degrees < thr_sw:
                val = "South-West"
             elif degrees >= thr_sw and degrees < thr_s:
                val = "South"
             elif degrees >= thr_s and degrees < thr_se:
                val = "South-East"
             elif degrees >= thr_se and degrees < thr_e:
                val = "East"
             elif degrees >= thr_e and degrees < thr_ne:
                val =  "North-East"
          else :
             val = "Error"
             ret = ret + 2
       except :
          ret = ret + 1
       return (val,ret)
