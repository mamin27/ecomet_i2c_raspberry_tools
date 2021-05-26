from __future__ import division
import logging
import time
import math
from i2c_pkg.pca9557_pkg import pca9557_constant

cmd_list = { 'REGISTER0' : pca9557_constant.REGISTER0, 'REGISTER1' : pca9557_constant.REGISTER1, 'REGISTER2' : pca9557_constant.REGISTER2, 'REGISTER3' : pca9557_constant.REGISTER3,
         }
# Input PIN Status
Sleep				= 10
Measure				= 2
Threshold			= 1
Init				= 0

# Offset Status
O_Init				= 0
O_Pending			= 1
O_Set				= 2

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
        self._iport = [ [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------']]
        self._oport = [ [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------'],
                        [10,Sleep,'X-------']]
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
    def port_init (self) :
        check_port = (self.read_register('REGISTER3')[0])
        self._logger.debug('binary_status: 0b%s','{0:b}'.format(check_port))
        idx_i = 0
        idx_o = 0
        for i in range(8) :
            bit = self.get_bit(check_port,i)
            if (bit == 0b1 and (idx_i <= 7 or idx_o <=7)) :
                self._iport[idx_i] = [i,Measure,'X-------']
                idx_i = idx_i + 1
            else :
                self._oport[idx_o] = [i,Measure,'X-------']
                idx_o = idx_o + 1
        if (idx_i == 7 ) : self._iport[idx_i] = [i,Measure,'X-------']
        if (idx_o == 7 ) : self._iport[idx_o] = [i,Measure,'X-------']
        self._logger.debug('init input ports: %s','{}'.format(self._iport))
        self._logger.debug('init output ports: %s','{}'.format(self._oport))
        return 0
    def port_show_name (self, setting = 'io') :
        arr = [[ 'X-------','NOT INIT'],[ 'X-------','NOT INIT'],[ 'X-------','NOT INIT'],[ 'X-------','NOT INIT'],
               [ 'X-------','NOT INIT'],[ 'X-------','NOT INIT'],[ 'X-------','NOT INIT'],[ 'X-------','NOT INIT']]
        for j in range(8) :
          for i in range(9) :
            if  (i == 8) :
               self._logger.debug('ports are not currently initialized')
               return (arr,1)
            if ( self._iport[i][0] == j  and (setting == 'io' or setting == 'i')) :
               if ( self._iport[i][2] != 'X-------' ) :
                  arr[j] = [ self._iport[i][2],'INPUT' ]
                  break
               else : 
                  arr[j][1] = 'INPUT'
                  break
            elif  ( self._oport[i][0] == j  and setting == 'i' ) :
               arr[j] = ['--------','OUTPUT']
               break
            elif (self._oport[i][0] == j and (setting == 'io' or setting == 'o') ):
               if ( self._oport[i][2] != 'X-------' ) :
                  arr[j] = [ self._oport[i][2],'OUTPUT' ]
                  break
               else :
                  arr[j][1] = 'OUTPUT'
                  break
            elif ( self._iport[i][0] == j  and setting == 'o' ) :
               arr[j] = ['--------','INPUT']
               break
        return (arr,0)
    def reset_inputs (self) :
        for i in self._iport :
           if ( i[1] != Sleep ) :
              i[1] = Init
    def read_input_port (self, thr = '->0', mtime = 10, offset = 0) :
        self.reset_inputs()
        from time import sleep
        start = time.time()
        check_port = self.read_register('REGISTER3')[0]
        self._logger.debug('check_port: 0b%s','{0:b}'.format(check_port))
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
        thr_reached = O_Init
        self._logger.debug('INIT: ' + str(self._iport))
        while True :
           idx = 0
           for tst_port in self._iport :
               if ( tst_port[1] == Measure or tst_port[1] == Init) :
                   if ( self.get_bit(self.read_register('REGISTER0')[0],tst_port[0]) == 0b0 ) :
                       self._iport[idx][1] = Threshold
                       thr_reached = O_Pending
                       measure = time.time()
               else :
                   break
               self._logger.debug(str(idx) + ': ' + str(self._iport))
               idx = idx + 1
           end = time.time()
           if ( thr_reached == O_Pending) :
              if ( end-measure > offset ) :
                 thr_reached = O_Init
                 #self._logger.info(end-measure)
                 return (self._iport,0)
           if (end-start > mtime ) :
              self._logger.debug('maximum measure time (mtime) reached!')
              return (self._iport,1)
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
       self.port_init()
       return(mask_byte,0)
    def set_io_name ( self, port_arr = None ) :
       if ( port_arr == None ) :
          return (1)
       for j in range(8) :
          for i in range(8) :
             if ( self._iport[i][0] == port_arr[j][0] ) :
                self._iport[i][2] = port_arr[j][1]
                break
             elif ( self._oport[i][0] == port_arr[j][0] ) :
                self._oport[i][2] = port_arr[j][1]
                break
       return (0)
