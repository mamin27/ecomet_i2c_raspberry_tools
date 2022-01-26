from __future__ import division
import logging
import re
import Adafruit_PureIO

# Platform identification constants.
plat_list = { 0 : 'UNKONWN',
              1 : 'RASPBERRY_PI',
              2 : 'BEAGLEBONE_BLACK',
              3 : 'MINNOWBOARD',
              4 : 'JETSON_NANO',
        }

class Board_plat(object):

   def __init__(self, address=None, busnum=None, arange=None, i2c=None, **kwargs) :
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            import ecomet_i2c_sensors.Platform as Platform
            i2c = I2C
            plat = Platform
        self._logger = logging.getLogger(__name__)
        self._plat = plat.platform_detect()
        self._pi_ver = plat.pi_version()
        self._pi_rev = plat.pi_revision()
        self._bus = i2c.get_default_bus()
        self._busnum = busnum
        self._slaves = ''
        if arange is None:
            arange = [0x00,0x77];
        for addr in range(arange[0],arange[1]) :
         ret = 0
         try :
           self._device = i2c.get_i2c_device(address=addr,busnum=self._busnum, **kwargs)
         except :
           ret = 1
         if addr == 0x76 :  #special detection for ms5637 chip
            try :
             self._device.writeRaw8(0x1E)
            except :
              ret = 3 
         else:
            try :
              self._device.readRaw8()
            except :
              ret = 2
         if ret == 0 :
           self._slaves = self._slaves + str(hex(addr)) + ':'
        self._slaves = self._slaves[:-1]
   def board (self) :
       version = plat_list[self._plat]
       if version == 'RASPBERRY_PI' :
          if re.search('\.',self.pi_ver()) :
             version = version +  self.pi_ver()
          else :
             version = version +  self.pi_ver() + '.' + self.pi_rev()
       return version
   def pi_ver (self) :
       return str(self._pi_ver)
   def pi_rev (self) :
       return str(self._pi_rev)
   def bus (self) :
       return str(self._bus)
   def slaves (self) :
       return self._slaves
