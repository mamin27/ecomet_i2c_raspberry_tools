from __future__ import division
import logging
import time
import random
import os
import pickle
from i2c_pkg.ina260_pkg import ina260,ina260_constant,ina260_ui_constant

class INA260_UI(object):
    '''INA260_UI()'''

    def __init__(self, chip=0, time = 1, **kwargs) :
       self._logger = logging.getLogger(__name__)
       if chip == 0 :
          self._address = ina260_constant.INA260_ADDRESS1 
          _mconst = ina260_ui_constant.set_measure_0
       elif chip == 1 :
          self._address = ina260_constant.INA260_ADDRESS2
          _mconst = ina260_ui_constant.set_measure_1
       _ina = ina260.INA260(address=self._address)
       self._logger.debug("address: %d" % self._address)
       self._ina = _ina
       self._measure_avgc = _ina.write_funct('AVGC', value = _mconst.AVGC)
       self._measure_ishct = _ina.write_funct('ISHCT', value = _mconst.ISHCT)
       self._measure_vbusct = _ina.write_funct('VBUSCT', value = _mconst.VBUSCT)
       self._measure_mode = _ina.write_funct('MODE', value = _mconst.MODE)
       r = random.randrange(3,999,3)
       self._filename = 'ina260_' + str(r)
       self._logger.debug("filename: %s" % self._filename)
       self._stime = time

    def child(self):
      fd = open(self._filename,'wb')
      self._logger.debug("child: %d" % os.getpid())
      voltage = self._ina.measure_voltage(stime = self._stime)
      pickle.dump(voltage, fd,-1)
      fd.close()
      os._exit(0)

    def parent(self):
      while True:
         newpid = os.fork()
         if newpid == 0:
            self.child()
         else:
            self._logger.debug("parent: %d" % os.getpid())
            current = self._ina.measure_current(stime = self._stime)
            os.waitid(os.P_PID,newpid,os.WEXITED)
            break
      fd = open(self._filename,'rb')
      voltage = pickle.load(fd)
      fd.close()
      os.remove(self._filename)

      multi_measure = [current,voltage]
      return (multi_measure)
   
    def measure_ui (self) :
       data = {}
       data = self.parent()
       return data
