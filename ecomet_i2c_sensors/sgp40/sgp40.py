''' 
  @note Origin Code
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [yangfeng]<feng.yang@dfrobot.com> 
  version  V1.0
  date  2021-01-15
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_SGP40
  
  Updated Code: 2024-03-13
  Copyright (c) 2024 eComet Co.Ltd (https://twitter.com/mminar7)
  @author      <mminar7@gmail.com>
  @license	   GPL-3.0
'''

from time import sleep, time
import smbus2
import logging
from ecomet_i2c_sensors.sgp40 import sgp40_algorithm, sgp40_constant
from ecomet_i2c_sensors.sgp40.sgp40_algorithm import VOCAlgorithm

reg_list = { 'TEST_OK' : sgp40_constant.TEST_OK, 'HEATER_OFF' : sgp40_constant.HEATER_OFF,
             'MEASURE_TEST' : sgp40_constant.MEASURE_TEST, 'SOFT_RESET' : sgp40_constant.SOFT_RESET,
             'MEASURE_RAW' : sgp40_constant.MEASURE_RAW,
             'DURATION_READ_RAW_VOC' : sgp40_constant.DURATION_READ_RAW_VOC,
             'DURATION_WAIT_MEASURE_TEST' : sgp40_constant.DURATION_WAIT_MEASURE_TEST,
             'OFFSET' : sgp40_constant.OFFSET
        }

class SGP40:
    '''
      @brief Module init
      @param bus:int Set to IICBus
      @param relative_humidity:float Set to relative_humidity
      @param temperature_c:float Set to temperature
    '''
    def __init__(self,bus = 1,address=sgp40_constant.SGP40_ADDR, busnum=None, i2c=None, relative_humidity = 50,temperature_c = 25, **kwargs):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)  
        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface='smbus2', **kwargs)
        self._my_vocalgorithm = VOCAlgorithm()
        self._temperature_c = temperature_c
        self._relative_humidity = relative_humidity
        self._rh = 0
        self._temc = 0
        self._rh_h = 0
        self._rh_l = 0
        self._temc_h = 0
        self._temc_l = 0
        self._temc_crc = 0
        self._rh_crc = 0

    '''
      @brief Set temperature and humidity
      @param relative_humidity:float Set to relative_humidity
      @param temperature_c:float Set to temperature
    '''
    def set_envparams(self,relative_humidity,temperature_c):
        self._temperature_c = temperature_c
        self._relative_humidity = relative_humidity

    '''
      @brief start equipment
      @param duration:int Set to Warm-up time
      @return equipment condition. 0: succeed  1: failed 
    '''
    def begin(self,duration = 10):
        self._my_vocalgorithm.vocalgorithm_init()
        timeOne = int(time())
        while(int(time())-timeOne<duration):
            self.get_voc_index()
        return self._measure_test()

    '''
      @brief Get raw data
      @param duration:int Set to Warm-up time
      @return collect result. (-1 collect failed)  (>0 the collection value)
    '''
    def measure_raw(self):
        self._data_transform()
        self.write_register('MEASURE_RAW',[self._rh_h,self._rh_l,self._rh_crc,self._temc_h,self._temc_l,self._temc_crc])
        sleep(reg_list['DURATION_READ_RAW_VOC'])
        raw,ret = self.read_register('OFFSET',byte = 3)
        if self._check_crc(raw) == 0:
          return raw[0]<<8 | raw[1]
        else:
          return -1

    '''
      @brief Measure VOC index after humidity compensation
      @n VOC index can indicate the quality of the air directly. The larger the value, the worse the air quality.
      @n   0-100,no need to ventilate, purify
      @n   100-200,no need to ventilate, purify
      @n   200-400,ventilate, purify
      @n   00-500,ventilate, purify intensely
      @param duration:int Set to Warm-up time
      @return The VOC index measured, ranged from 0 to 500
    '''
    def get_voc_index(self):
        raw = self.measure_raw()
        if raw<0:
            return -1
        else:
            vocIndex = self._my_vocalgorithm.vocalgorithm_process(raw)
            return vocIndex

    '''
      @brief Convert environment parameters
    '''
    def _data_transform(self):
        self._rh = int(((self._relative_humidity*65535)/100+0.5))
        self._temc = int(((self._temperature_c+45)*(65535/175)+0.5))
        self._rh_h = int(self._rh)>>8
        self._rh_l = int(self._rh)&0xFF
        self._rh_crc = self._crc(self._rh_h,self._rh_l)
        self._temc_h = int(self._temc)>>8
        self._temc_l = int(self._temc)&0xFF
        self._temc_crc = self._crc(self._temc_h,self._temc_l) 

    '''
      @brief Sensor self-test
      @n VOC index can indicate the quality of the air directly. The larger the value, the worse the air quality.
      @n   0-100,no need to ventilate, purify
      @n   100-200,no need to ventilate, purify
      @n   200-400,ventilate, purify
      @n   00-500,ventilate, purify intensely
      @param duration:int Set to Warm-up time
      @return self-test condition. 0: succeed; 1: failed 
    '''
    def _measure_test(self):
        self.write_register('MEASURE_TEST',[])
        #self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.CMD_MEASURE_TEST_H, [self.CMD_MEASURE_TEST_L])
        sleep(reg_list['DURATION_WAIT_MEASURE_TEST'])
        raw,ret = self.read_register('OFFSET',byte = 2)
        if raw[0] == (reg_list['TEST_OK'] >> 8) & 0xFF and raw[1] == (reg_list['TEST_OK'] & 0xFF) :
            return 0
        else:
            return 1

    def index_to_explanation(self,index) :
        if index < 80 :
            return 'excelent'
        elif index >= 80 and index < 180 :
            return 'normal'
        elif index >= 180 and index < 300 :
            return 'warning'
        elif index >= 300 and index < 400 :
            return 'major'
        elif index > 500 :
            return 'critical' 

    '''
      @brief Sensor reset
    '''
    def _reset(self):
        self.write_register('SOFT_RESET',[])

    '''
      @brief sgp40 Heater Off. Turn the hotplate off and stop the measurement. Subsequently, the sensor enters the idle mode.
    '''
    def _heater_off(self):
        self.write_register('HEATER_OFF',[])

    '''
      @brief Verify the calibration value of the sensor
      @param raw : list Parameter to check
      @return  Check result. -1: Check failed; 0: Check succeed
    '''
    def _check_crc(self, raw):
        assert (len(raw) == 3)
        if self._crc(raw[0], raw[1]) != raw[2]:
            return -1
        return 0

    '''
      @brief CRC
      @param data1  High 8 bits data
      @param data2  LOW 8 bits data
      @return  Calibration value
    '''
    def _crc(self,data_1,data_2):
        crc = 0xff
        list = [data_1,data_2]
        for i in range(0,2):
            crc = crc^list[i]
            for bit in range(0,8):
                if(crc&0x80):
                    crc = ((crc <<1)^0x31)
                else:
                    crc = (crc<<1)
            crc = crc&0xFF
        return crc

    def read_register(self, register, byte=None) :
       reg_status = -9999
       ret = 0
       if register in ['OFFSET'] :
          try :
             reg_status = self._device.readList(reg_list[register],byte)
          except :
             ret = ret + 1
       return(reg_status,ret)

    def write_register(self, register,data) :
       ret = 0
       #print ( register )
       if register in ['MEASURE_RAW','MEASURE_TEST','SOFT_RESET','SOFT_RESET'] :
          _hi = (reg_list[register] >> 8) & 0xFF
          _lo = reg_list[register] & 0xFF
          data = [_lo] + data 
          try :
             self._device.writeList(_hi,data) 
          except :
             ret = ret + 1
       return (ret)
