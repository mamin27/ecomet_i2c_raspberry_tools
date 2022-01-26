from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.ms5637 import ms5637_constant

cmd_list = { 'RESET' : ms5637_constant.RESET, 
             'D1_CONV_256' : ms5637_constant.D1_CONV_256, 'D1_CONV_512' : ms5637_constant.D1_CONV_512, 'D1_CONV_1024' : ms5637_constant.D1_CONV_1024, 'D1_CONV_2048' : ms5637_constant.D1_CONV_2048,
             'D1_CONV_4096' : ms5637_constant.D1_CONV_4096, 'D1_CONV_8192' : ms5637_constant.D1_CONV_8192,
             'D2_CONV_256' : ms5637_constant.D2_CONV_256, 'D2_CONV_512' : ms5637_constant.D2_CONV_512, 'D2_CONV_1024' : ms5637_constant.D2_CONV_1024, 'D2_CONV_2048' : ms5637_constant.D2_CONV_2048,
             'D2_CONV_4096' : ms5637_constant.D2_CONV_4096, 'D2_CONV_8192' : ms5637_constant.D2_CONV_8192,
             'ADC_READ' : ms5637_constant.ADC_READ,
             'PROM_PRE_SENS' : ms5637_constant.PROM_PRE_SENS, 'PROM_PRE_OFFSET' : ms5637_constant.PROM_PRE_OFFSET, 'PROM_TMP_PRE_SENS' : ms5637_constant.PROM_TMP_PRE_SENS, 'PROM_TMP_PRE_OFFSET' : ms5637_constant.PROM_TMP_PRE_OFFSET,
             'PROM_REF' : ms5637_constant.PROM_REF, 'PROM_TMP_COEF' : ms5637_constant.PROM_TMP_COEF,
             'CONV_256_TIME' : ms5637_constant.CONV_256_TIME , 'CONV_512_TIME' : ms5637_constant.CONV_512_TIME , 'CONV_1024_TIME' : ms5637_constant.CONV_1024_TIME , 
             'CONV_2048_TIME' : ms5637_constant.CONV_2048_TIME , 'CONV_4096_TIME' : ms5637_constant.CONV_4096_TIME , 'CONV_8192_TIME' : ms5637_constant.CONV_8192_TIME
        }

logger = logging.getLogger(__name__) 


class MS5637(object):
    '''MS5637() micro altimeter. It is optimized for  altimeter  and  barometer  applications.'''

    def __init__(self, address=ms5637_constant.MS5637_ADDRESS, busnum=ms5637_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the MS5637.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self.c1 = self.read_register('PROM_PRE_SENS')
        self.c2 = self.read_register('PROM_PRE_OFFSET')
        self.c3 = self.read_register('PROM_TMP_PRE_SENS')
        self.c4 = self.read_register('PROM_TMP_PRE_OFFSET')
        self.c5 = self.read_register('PROM_REF')
        self.c6 = self.read_register('PROM_TMP_COEF')
        self.d1_time = cmd_list['CONV_256_TIME']
        self.d2_time = cmd_list['CONV_512_TIME']
        self.d3_time = cmd_list['CONV_1024_TIME']
        self.d4_time = cmd_list['CONV_2048_TIME']
        self.d5_time = cmd_list['CONV_4096_TIME']
        self.d6_time = cmd_list['CONV_8192_TIME']
    def sw_reset (self) :
        ret = 0
        try:
            self.write_register('RESET', stime = 0)
        except :
            ret = ret + 1
            self._logger.debug('write error')
        from time import sleep
        sleep(0.1) # wait for done sw reset
        return ret
    def read_register(self, register) :
        if register in ['PROM_PRE_SENS','PROM_PRE_OFFSET','PROM_TMP_PRE_SENS','PROM_TMP_PRE_OFFSET','PROM_REF','PROM_TMP_COEF'] :
           ret = 0
           reg_type = 2
           try :
              reg_status_bita = self._device.readList(cmd_list[register],2)
              if not reg_status_bita:
                return (0x00,2)
              reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0])
              reg_status = int(reg_status_hex, 0)
           except :
              ret = ret + 1
        elif register in ['ADC_READ'] :
           ret = 0
           reg_type = 3
           try :
              reg_status_bita = self._device.readList(cmd_list[register],3)
           except :
              ret = ret + 1
        if ret > 0 :
           self._logger.debug('read_register %s failed (%s)',register,ret)
           return (0,ret)
        else :
           if reg_type == 2 :
             self._logger.debug('lo_byte %s, hi_byte %s', '{0:02x}'.format(reg_status_bita[1]), '{0:02x}'.format(reg_status_bita[0]))
             reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0]) + '{0:02x}'.format(reg_status_bita[1])
             self._logger.debug('2 bytes read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
             reg_status = reg_status_bita[0] * 256 + reg_status_bita[1]
             self._logger.debug('read_register, status: %s', '{0}'.format(reg_status))
             return (reg_status, ret)
           if reg_type == 3 :
             self._logger.debug('lo_byte %s, mid_byte %s hi_byte %s', '{0:02x}'.format(reg_status_bita[2]),'{0:02x}'.format(reg_status_bita[1]), '{0:02x}'.format(reg_status_bita[0]))
             reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0]) + '{0:02x}'.format(reg_status_bita[1]) + '{0:02x}'.format(reg_status_bita[2])
             self._logger.debug('3 bytes read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
             reg_status = reg_status_bita[0] * 65536 + reg_status_bita[1] * 256 + reg_status_bita[2]
             self._logger.debug('read_register, status: %s', '{0}'.format(reg_status))
             return (reg_status, ret)
    def write_register(self, register, stime = 500) :
        if register in ['RESET','D1_CONV_256','D1_CONV_512','D1_CONV_1024','D1_CONV_2048','D1_CONV_4096','D1_CONV_8192',
                                'D2_CONV_256','D2_CONV_512','D2_CONV_1024','D2_CONV_2048','D2_CONV_4096','D2_CONV_8192'] :
           ret = 0
           offset = 0.02
           try:
               self._device.writeRaw8(cmd_list[register])
           except :
               ret = ret + 1
               self._logger.debug('write error to reg [{}]'.format(register))
           from time import sleep
           self._logger.debug("wait: {}".format(stime * 0.001 + offset))
           sleep(stime * 0.001 + offset) # wait for done sw reset
           return ret
        else :
           self._logger.debug('wrong reg name [{}]'.format(register))
           return 100
    def measure (self, accuracy = 1) :
        ret = 0
        if (accuracy == 1) :
           self.write_register('D2_CONV_256', stime = self.d1_time)
           D2 = self.read_register('ADC_READ')[0]
           self.write_register('D1_CONV_256', stime = self.d1_time)
           D1 = self.read_register('ADC_READ')[0]
        elif (accuracy == 2) :
           self.write_register('D2_CONV_512', stime = self.d2_time)
           D2 = self.read_register('ADC_READ')[0]
           self.write_register('D1_CONV_512', stime = self.d2_time)
           D1 = self.read_register('ADC_READ')[0]
        elif (accuracy == 3) :
           self.write_register('D2_CONV_1024', stime = self.d3_time)
           D2 = self.read_register('ADC_READ')[0]
           self.write_register('D1_CONV_1024', stime = self.d3_time)
           D1 = self.read_register('ADC_READ')[0]
        elif (accuracy == 4) :
           self.write_register('D2_CONV_2048', stime = self.d4_time)
           D2 = self.read_register('ADC_READ')[0]
           self.write_register('D1_CONV_2048', stime = self.d4_time)
           D1 = self.read_register('ADC_READ')[0]
        elif (accuracy == 5) :
           self.write_register('D2_CONV_4096', stime = self.d5_time)
           D2 = self.read_register('ADC_READ')[0]
           self.write_register('D1_CONV_4096', stime = self.d5_time)
           D1 = self.read_register('ADC_READ')[0]
        elif (accuracy == 6) :
           self.write_register('D2_CONV_8192', stime = self.d6_time)
           D2 = self.read_register('ADC_READ')[0]
           self.write_register('D1_CONV_8192', stime = self.d6_time)
           D1 = self.read_register('ADC_READ')[0]
        else :
           self._logger.info("wrong accuracy range, only from 1-6")
           ret = 1
           return (-1000,-1000,-1000,ret)
        dT = D2 - self.c5[0] * 2**8
        temp = 2000 + dT * self.c6[0] / 2**23
        OFF = self.c2[0] * 2**17 + (self.c4[0] * dT) / 2**6
        SENS = self.c1[0] * 2**16 + (self.c3[0] * dT ) / 2**7
        T2 = 0
        OFF2 = 0
        SENS2 = 0

        if temp > 2000 :
           T2 = 5 * dT**2 / 2**38
           OFF2 = 0
           SENS2 = 0
        elif temp < 2000 :
           T2 = 3 * (dT**2) / 2**33
           OFF2 = 61 * ((temp - 2000)**2) / 2**4
           SENS2 = 29 * ((temp - 2000)**2) / 2**4
           if temp < -1500 :
              OFF2 = OFF2 + 17 * ((temp + 1500)**2)
              SENS2 = SENS2 + 9 * ((temp + 1500)**2)
        temp = temp - T2
        OFF = OFF - OFF2
        SENS = SENS - SENS2
        tempc = temp/100
        tempf = tempc * 1.8 + 32
        pressure = ((((D1 * SENS) / 2**21) - OFF) / 2**15) / 100.0
        return(tempc,tempf,pressure,ret)
