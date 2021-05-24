from __future__ import division
import logging
import time
import math
from i2c_pkg.pca9557_pkg import pca9557_constant

cmd_list = { 'REGISTER0' : pca9557_constant.REGISTER0, 'REGISTER1' : pca9557_constant.REGISTER1, 'REGISTER2' : pca9557_constant.REGISTER2, 'REGISTER3' : pca9557_constant.REGISTER3,
         }

logger = logging.getLogger(__name__) 


class PCA9557(object):
    '''PCA9557() micro altimeter. It is optimized for  altimeter  and  barometer  applications.'''

    def __init__(self, address=pca9557_constant.PCA9557_ADDRESS, busnum=pca9557_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the MS5637.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import i2c_pkg.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self.reg0 = self.read_register('REGISTER0')
        self._iport = [ [10,2],
                        [10,2],
                        [10,2],
                        [10,2],
                        [10,2],
                        [10,2],
                        [10,2],
                        [10,2] ]
        self._bin_to_hex = {
                0 : 1,
                1 : 2,
                2 : 4,
                3 : 8,
                4 : 16,
                5 : 32,
                6 : 64,
                7 : 128 }
    def sw_reset (self) :
        ret = 0
        try:
            self.write_register('REGISTER1', value = 0)
            self.write_register('REGISTER2', value = 240)
            self.write_register('REGISTER3', value = 255)
        except :
            ret = ret + 1
            self._logger.debug('write error')
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def read_register(self, register) :
        if register in ['REGISTER0','REGISTER1','REGISTER2','REGISTER3'] :
           ret = 0
           try :
              reg_status_bita = self._device.readList(cmd_list[register],1)
              if not reg_status_bita:
                return (0x00,1)
              reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0])
              reg_status = int(reg_status_hex, 0)
           except :
              ret = ret + 1
        if ret > 0 :
           self._logger.debug('read_register %s failed (%s)',register,ret)
           return (0,ret)
        else :
           reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0])
           self._logger.debug('byte read_register, reg_status: %s', '{0}'.format(reg_status_hex))
           reg_status = reg_status_bita[0]
           self._logger.debug('read_register, status: %s', '{0}'.format(reg_status))
           return (reg_status, ret)
    def write_register(self, register, value = 0) :
        if register in ['REGISTER0','REGISTER1','REGISTER2','REGISTER3'] :
           ret = 0
           offset = 0.0003 #min 200 ns
           try:
               self._device.write8(cmd_list[register],value)
           except :
               ret = ret + 1
               self._logger.debug('write error to reg [{}]'.format(register))
           from time import sleep
           sleep(offset) # wait for done sw reset
           return ret
        else :
           self._logger.debug('wrong reg name [{}]'.format(register))
           return 100
    def get_bit(self, byte, bit_idx) :
        return 1 if (byte & ( 1 << bit_idx) > 0) else 0
    def read_input_port (self, thr = '->0', mtime = 10, offset = 0) :
        check_port = (self.read_register('REGISTER3')[0])
        self._logger.debug('binary_status: 0b%s','{0:b}'.format(check_port))
        idx = 0
        for i in range(8) :
            bit = self.get_bit(check_port,i)
            if (bit == 0b1 and idx <= 7) :
                self._iport[idx] = [i,1]
                idx = idx + 1
        if (idx == 7) : self._iport[idx] = [i,2]
        mask_byte = 0
        if (thr == '->0') :
          for i in range(8) :
             if ( self.get_bit(check_port,i) == 0 ):
                mask_byte = mask_byte + self._bin_to_hex[i]
        elif (thr == '->1') :
          for i in range(8) :
             if ( self.get_bit(check_port,i) == 1 ):
                mask_byte = mask_byte + self._bin_to_hex[i]
        else :
          self._logger.debug('wrong setting of thr parameter, ->0 or ->1 possible')
          return (self._iport,2)
        self._logger.debug('mask_byte: 0b%s','{0:b}'.format(mask_byte))
        self.write_register(register = 'REGISTER2', value = mask_byte)
        from time import sleep
        start = time.time()
        thr_reached = False
        self._logger.debug('INIT: ' + str(self._iport))
        while True :
           idx = 0
           for tst_port in self._iport :
               if ( tst_port[1] != 2 ) :
                   time.sleep(offset)
                   if ( self.get_bit(self.read_register('REGISTER0')[0],tst_port[0]) == 0b0 ) :
                       self._iport[idx][1] = 0
                       thr_reached = True
               else : break
               self._logger.debug(str(idx) + ': ' + str(self._iport))
               idx = idx + 1
           end = time.time()
           if (end-start > mtime or thr_reached ) :
              if ( end-start > mtime ) :
                self._logger.debug('maximum measure time (mtime) reached!')
                return (self._iport,1)
              return (self._iport,0)
    def set_io ( self, pattern ) :
       arr = list(pattern)
       if ( len(arr) > 8 ) :
         self._logger.debug('pattern longer than expected, max 8 characters')
         return(-10,1)
       mask_byte = 0
       for i in range(8) :
         if ( arr[i] == 'I' ) :
            mask_byte = mask_byte + self._bin_to_hex[i]
         elif ( arr[i] != 'O' ) :
           self._logger.debug('wrong letter in pattern, only I or O accepted')
           return(mask_byte,2)
       self._logger.debug('Translated pattern: 0b%s','{0:b}'.format(mask_byte))
       self.write_register(register = 'REGISTER3', value = mask_byte)
       return(mask_byte,0)
