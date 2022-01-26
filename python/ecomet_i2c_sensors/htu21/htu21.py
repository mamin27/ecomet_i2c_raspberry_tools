from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.htu21 import htu21_constant

A = 8.1332
B = 1762.39
C = 235.66

reg_list = { 'TEMP' : htu21_constant.TEMP, 'HUMDT' :  htu21_constant.HUMDT, 
             'WRITE_USER' : htu21_constant.WRITE_USER, 'READ_USER' : htu21_constant.READ_USER, 'SRESET' : htu21_constant.SRESET,
        }
conf_bit_on_list = { 'MEAS_RES1' : htu21_constant.MEAS_RES1,
                     'MEAS_RES2' : htu21_constant.MEAS_RES2,
                     'MEAS_RES3' : htu21_constant.MEAS_RES3,
                     'MEAS_RES4' : htu21_constant.MEAS_RES4,
                     'BTST_HI' : htu21_constant.BTST_HI,
                     'BTST_LO' : htu21_constant.BTST_LO,
                     'HEAT_DISABLE' : htu21_constant.HEAT_DISABLE,
                     'HEAT_ENABLE' : htu21_constant.HEAT_ENABLE,
                     'OTP_RELOAD_DISABLE' : htu21_constant.OTP_RELOAD_DISABLE,
                     'OTP_RELOAD_ENABLE' : htu21_constant.OTP_RELOAD_ENABLE,
                }

conf_bit_off_list = { 'MEAS_RES1_CLR' : htu21_constant.MEAS_RES1_CLR,
                      'MEAS_RES2_CLR' : htu21_constant.MEAS_RES2_CLR,
                      'MEAS_RES3_CLR' : htu21_constant.MEAS_RES3_CLR,
                      'MEAS_RES4_CLR' : htu21_constant.MEAS_RES4_CLR,
                      'BTST_HI_CLR' : htu21_constant.BTST_HI_CLR,
                      'BTST_LO_CLR' : htu21_constant.BTST_LO_CLR,
                      'HEAT_DISABLE_CLR' : htu21_constant.HEAT_DISABLE_CLR,
                      'HEAT_ENABLE_CLR' : htu21_constant.HEAT_ENABLE_CLR,
                      'OTP_CLR' : htu21_constant.OTP_CLR
                }
   
conf_mask_bit_list = { 'REG_MEAS' : htu21_constant.REG_MEAS,
                       'REG_BAT' : htu21_constant.REG_BAT,
                       'REG_HEAT' : htu21_constant.REG_HEAT,
                       'REG_OTP' : htu21_constant.REG_OTP
                      }                      
logger = logging.getLogger(__name__) 

def register_list() :

   hdc = HTU21()
   hdc._logger = logging.getLogger('ecomet.htu21.reglist') 
   register = {}
   
   reg_conf = {}
   reg_id = {}
   
   hres_switch = { 0: '12BIT',
                   1: '8BIT',
                   128: '10BIT',
                   129: '11BIT'}
   
   tres_switch = { 0: '14BIT',
                   1: '12BIT',
                   128: '13BIT',
                   129: '11BIT' }
                   
   reg_conf['HRES'] = hres_switch.get((hdc.read_register( register = 'READ_USER' )[0] & conf_mask_bit_list['REG_MEAS']))
   reg_conf['TRES'] = tres_switch.get((hdc.read_register( register = 'READ_USER' )[0] & conf_mask_bit_list['REG_MEAS']))
   reg_conf['BAT'] = 'LOW' if hdc.read_register( register = 'READ_USER' )[0] & conf_mask_bit_list['REG_BAT'] > 0 else 'GOOD'           
   reg_conf['HEAT'] = 'ENABLE' if hdc.read_register( register = 'READ_USER' )[0] & conf_mask_bit_list['REG_HEAT'] > 0 else 'DISABLE'
   reg_conf['OTP'] = 'DISABLE' if hdc.read_register( register = 'READ_USER' )[0] & conf_mask_bit_list['REG_OTP'] > 0 else 'ENABLE'  
   
   register['REG'] = reg_conf
   
   return (register);
  
def measure_list() :
   
   htu = HTU21()
   htu._logger = logging.getLogger('ecomet.htu21.reglist') 
   measure = {}
   mlist = {}
   ret = 0
   
   (mlist['TEMP'],nret) = htu.measure_temp()
   ret = ret + nret
   (mlist['HMDT'],nret) = htu.measure_hmdt()
   ret = ret + nret
   (mlist['DEW_POINT'],nret) = htu.dew_point()
   ret = ret + nret
     
   measure['MEASURE'] = mlist
   
   return (measure,ret)

class HTU21(object):
    '''htu21() PWM LED/servo controller.'''

    def __init__(self, address=htu21_constant.HTU21_ADDRESS, busnum=htu21_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the htu21.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
    def sw_reset (self) :
        register = 'SRESET'
        ret = 0
        try:
           self._device.writeRaw8(reg_list[register])
        except :
           ret = 1
        from time import sleep
        sleep(0.02) # wait for done sw reset
        return ret
    def battery (self) :
        (reg_status,ret) = self.read_register( register = 'READ_USER' )
        reg_status = reg_status & conf_bit_on_list['BTST_LO']
        if reg_status > 0 :
            ret = 1
        else :
            ret = 0
        return ret
    def read_register(self, register) :
        if register == 'TEMP' or register == 'HUMDT' or register == 'READ_USER' or register == 'WRITE_USER' :
           ret = 0
           if register == 'WRITE_USER' :
              register = 'READ_USER'
           try:
              self._device.writeRaw8(reg_list[register])		   
              reg_status_bit = self._device.readU8(reg_list[register])
              reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bit)
              reg_status = int(reg_status_hex, 0)
           except :
              ret = ret + 1;
              self._logger.debug('error')
           if ret > 1 :
              self._logger.debug('read_register %s failed (%s)',register,ret)
              return (0x00,ret)
           else :
              self._logger.debug('read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
              self._logger.debug('read_register %s, binary data: %s%s', register, 'bx','{0:b}'.format(reg_status))
              return (reg_status,0)
    def write_register(self, register, bits) :
          ret = 0
          (reg_status,ret) = self.read_register( register = register )
          if register == 'WRITE_USER' :
           for ibit in bits :
               bit_clr = ibit + '_CLR'
               reg_status = reg_status & conf_bit_off_list[bit_clr]
               self._logger.debug('write_register, init reg_status: %s, bit_mask_reg %s', '{0:02X}'.format(reg_status), format(bit_clr))
               reg_status = reg_status | conf_bit_on_list[ibit]
               self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), '{0:02X}'.format(conf_bit_on_list[ibit]))
           reg_status = reg_status & 0xff
           try :
               self._device.writeRaw8(reg_list[register])
               self._device.write8(reg_list[register],reg_status)
           except :
               ret = ret + 1
               self._logger.debug('writelist error')
          else :
              ret = 1
          if ret > 1 :
             self._logger.debug('write_register %s failed (%s)', register, ret)
          else :
             self._logger.debug('write_register %s, byte data: %s', register,reg_status)
          return ret
    def measure_temp (self) :
        byt_reg = ()
        register = 'TEMP'
        ret = 0
        from time import sleep
        try :
          self._device.writeRaw8(reg_list[register])
        except :
          ret = ret + 1
          self._logger.debug('temp measure error')
        for wait in range(100) :
          sleep(0.03)
          #self._logger.debug('loop %s', wait)
          try :
            reg_status_bita = self._device.readList(reg_list[register],3)
          except :
            pass
          else :
            break
        temp_status = reg_status_bita[1] & 0x03 
        self._logger.debug('temp measure status: %s',temp_status)
        if temp_status != 0 :
          ret = ret + 1
        temp_bin = '0b' + '{0:08b}'.format(reg_status_bita[0]) + '{0:06b}'.format(reg_status_bita[1] >> 2) + '00'
        self._logger.debug('temp measure binary output: %s',temp_bin)
        temp = int(temp_bin, 0)
        cksum_hex =  '0x' + '{0:02x}'.format(reg_status_bita[2])
        cksum = int(cksum_hex,0)
        temp = -46.85 + 175.72 * (temp/math.pow(2,16))
        self._logger.debug('temp measure output: %s','{0}'.format(temp))
        self._logger.debug('cksum: %s','{0}'.format(cksum))
        return (temp,ret)
    def measure_hmdt (self) :
        byt_reg = ()
        register = 'HUMDT'
        ret = 0
        from time import sleep
        try :
          self._device.writeRaw8(reg_list[register])
        except :
          ret = ret + 1
          self._logger.debug('humdt measure error')
        for wait in range(100) :
          sleep(0.03)
          #self._logger.debug('loop %s', wait)
          try :
            reg_status_bita = self._device.readList(reg_list[register],3)
          except :
            pass
          else :
            break
        hmdt_status = reg_status_bita[1] & 0x03
        self._logger.debug('humdt measure status: %s',hmdt_status)
        if hmdt_status != 2 :
          ret = ret + 1
        hmdt_bin = '0b' + '{0:08b}'.format(reg_status_bita[0]) + '{0:06b}'.format(reg_status_bita[1] >> 2) + '00'
        self._logger.debug('humdt measure binary output: %s',hmdt_bin)
        hmdt = int(hmdt_bin, 0)
        cksum_hex =  '0x' + '{0:02x}'.format(reg_status_bita[2])
        cksum = int(cksum_hex,0)
        hmdt = -6 + 125 * (hmdt/math.pow(2,16))
        self._logger.debug('humdt measure output: %s','{0}'.format(hmdt))
        self._logger.debug('cksum: %s','{0}'.format(cksum))
        return (hmdt,ret)
    def dew_point (self) :
        ret = 0
        try :
           temp = self.measure_temp()[0]
           hmdt = self.measure_hmdt()[0]
        except :
           ret = ret + 1
        pp = math.pow(10,A - (B / (temp + C)))
        dewp = - (( B / (math.log10(hmdt * (pp/100)) - A )) + C )
        return (dewp,ret)
