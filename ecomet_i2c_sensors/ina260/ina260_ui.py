from __future__ import division
import logging
import time
import random
import os
import pickle
import re
from ecomet_i2c_sensors.ina260 import ina260,ina260_constant,ina260_ui_constant

class INA260_UI(object):
    '''INA260_UI()'''
    '''chip=0#0x40'''

    def __init__(self, chip=0, time = 1, i_unit = 'mA', v_unit = 'mV', avgc = None, ishct = None, vbusct = None, mode = None, **kwargs) :
       self._logger = logging.getLogger(__name__)
       if chip == 0 :
          self._address = ina260_constant.INA260_ADDRESS1 
          _mconst = ina260_ui_constant.set_measure_0
          if avgc :
             _mconst.AVGC = avgc
          if ishct :
             _mconst.ISHCT = ishct
          if vbusct :
             _mconst.VBUSCT = vbusct
          if mode :
             _mconst.MODE = mode
       elif chip == 1 :
          self._address = ina260_constant.INA260_ADDRESS2
          _mconst = ina260_ui_constant.set_measure_1
          if avgc :
             _mconst.AVGC = avgc
          if ishct :
             _mconst.ISHCT = ishct
          if vbusct :
             _mconst.VBUSCT = vbusct
          if mode :
             _mconst.MODE = mode
       else :
          match = re.search('^(\d+)#(.+)$', chip,re.IGNORECASE)
          if match.group(1) == '0' :    
             self._address = int(match.group(2),16)
             _mconst = ina260_ui_constant.set_measure_0
             if avgc :
               _mconst.AVGC = avgc
             if ishct :
               _mconst.ISHCT = ishct
             if vbusct :
               _mconst.VBUSCT = vbusct
             if mode :
               _mconst.MODE = mode
          elif match.group(1) == '1' :
             self._address = int(match.group(2),16)
             _mconst = ina260_ui_constant.set_measure_1
             if avgc :
               _mconst.AVGC = avgc
             if ishct :
               _mconst.ISHCT = ishct
             if vbusct :
               _mconst.VBUSCT = vbusct
             if mode :
               _mconst.MODE = mode
       _ina = ina260.INA260(address=self._address)
       self._logger.debug("address: %d" % self._address)
       self._ina = _ina
       self._iunit = i_unit
       self._vunit = v_unit
       self._measure_avgc = _ina.write_funct('AVGC', value = _mconst.AVGC)
       self._measure_ishct = _ina.write_funct('ISHCT', value = _mconst.ISHCT)
       self._measure_vbusct = _ina.write_funct('VBUSCT', value = _mconst.VBUSCT)
       print ('Mode: {}'.format(_mconst.MODE))
       self._measure_mode = _ina.write_funct('MODE', value = _mconst.MODE)
       r = random.randrange(3,999,3)
       self._filename = 'ina260_' + str(r)
       self._logger.debug("filename: %s" % self._filename)
       self._stime = time

    def set_mode(self,s_mode='Cur-Volt-Continued',s_avg=1,s_vbusct='140us',s_vishct='140us') :
        ret = 0
        try:
           self.write_funct ('MODE', self._mode[s_mode])
        except:
           ret = 1
        return ret

    def child(self, vunit=None):
      if not vunit:
           vunit = self._vunit
      fd = open(self._filename,'wb')
      self._logger.debug("child: %d" % os.getpid())
      voltage = self._ina.measure_voltage(stime = self._stime, unit = vunit)
      pickle.dump(voltage, fd,-1)
      fd.close()
      os._exit(0)

    def parent(self, stime=None, iunit=None, vunit=None):
      if not stime:
           stime = self._stime
      if not iunit:
           iunit = self._iunit
      while True:
         newpid = os.fork()
         if newpid == 0:
            self.child( vunit = vunit)
         else:
            self._logger.debug("parent: %d" % os.getpid())
            current = self._ina.measure_current(stime = stime, unit = iunit )
            os.waitid(os.P_PID,newpid,os.WEXITED)
            break
      fd = open(self._filename,'rb')
      voltage = pickle.load(fd)
      fd.close()
      os.remove(self._filename)

      multi_measure = [current,voltage]
      return (multi_measure)

    def parent_i(self, stime=None, iunit=None):
      if not stime:
           stime = self._stime
      if not iunit:
           iunit = self._iunit
      current = self._ina.measure_current(stime = stime, unit = iunit )
      return (current)

    def parent_u(self, stime=None, vunit=None):
      if not stime:
           stime = self._stime
      if not vunit:
           vunit = self._vunit
      voltage = self._ina.measure_voltage(stime = self._stime, unit = vunit)
      return (voltage)

    def measure_ui (self, iunit=None, vunit=None) :
       if not iunit:
           iunit = self._iunit
       if not vunit:
           vunit = self._vunit
       data = {}
       data = self.parent( iunit = iunit, vunit = vunit)
       return data

    def measure_i (self, iunit=None) :
       if not iunit:
           iunit = self._iunit
       data = {}
       data = self.parent_i( iunit = iunit )
       return data

    def measure_u (self, vunit=None) :
       if not vunit:
           vunit = self._vunit
       data = {}
       data = self.parent_u( vunit = vunit )
       return data