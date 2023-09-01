from __future__ import division
import logging
import time
import math
from tsl2591 import tsl2591_constant
#from ecomet_i2c_sensors.tsl2591 import tsl2591_constant

INI_PIN             = 3

reg_list = { 'COMMAND' : tsl2591_constant.COMMAND_BIT,'ENABLE' : tsl2591_constant.ENABLE,'CONTROL' : tsl2591_constant.CONTROL, 'STATUS' : tsl2591_constant.STATUS,
			 'THR_AI_LTL' :  tsl2591_constant.THR_AI_LTL, 'THR_AI_LTH' : tsl2591_constant.THR_AI_LTH,'THR_AI_HTL' : tsl2591_constant.THR_AI_HTL,'THR_AI_HTH' : tsl2591_constant.THR_AI_HTH, 
			 'THR_NPAI_LTL' :  tsl2591_constant.THR_NPAI_LTL, 'THR_NPAI_LTH' : tsl2591_constant.THR_NPAI_LTH,'THR_NPAI_HTL' : tsl2591_constant.THR_NPAI_HTL,'THR_NPAI_HTH' : tsl2591_constant.THR_NPAI_HTH,
			 'PERSIST_FILTER' :  tsl2591_constant.PERSIST_FILTER, 'PACKAGE_PID' : tsl2591_constant.PACKAGE_PID,
			 'DEVICE_ID' : tsl2591_constant.DEVICE_ID,'DEVICE_STATUS' : tsl2591_constant.DEVICE_STATUS,
			 'CHAN0_L' : tsl2591_constant.CHAN0_L,'CHAN0_H' : tsl2591_constant.CHAN0_H,
			 'CHAN1_L' : tsl2591_constant.CHAN1_L,'CHAN1_H' : tsl2591_constant.CHAN1_H
        }
enable_mask_list =    { 'ENABLE_NPIEN' :  tsl2591_constant.ENABLE_NPIEN,
                     'ENABLE_SAI' : tsl2591_constant.ENABLE_SAI,
                     'ENABLE_AIEN' :  tsl2591_constant.ENABLE_AIEN,
                     'ENABLE_AEN' :  tsl2591_constant.ENABLE_AEN,
                     'ENABLE_POWER' : tsl2591_constant.ENABLE_POWER,
                     'DISABLE_NPIEN' :  tsl2591_constant.DISABLE_NPIEN,
                     'DISABLE_SAI' : tsl2591_constant.DISABLE_SAI,
                     'DISABLE_AIEN' :  tsl2591_constant.DISABLE_AIEN,
                     'DISABLE_AEN' :  tsl2591_constant.DISABLE_AEN,
                     'DISABLE_POWER' : tsl2591_constant.DISABLE_POWER
                }

ctrl_mask_list =	  { 'CTLR_RESET' : tsl2591_constant.CTLR_RESET,
					  'CTLR_AGAIN' : tsl2591_constant.CTLR_AGAIN,
					  'CTLR_ATIME' : tsl2591_constant.CTLR_ATIME
				}

persist_mask_list =   { 'PERSIST' : tsl2591_constant.CTLR_ATIME }
pid_mask_list =       { 'PID' : tsl2591_constant.PID_MASK }
status_mask_list =    { 'NPINTR_MASK' : tsl2591_constant.NPINTR_MASK,
						'AINT_MASK' : tsl2591_constant.AINT_MASK,
						'AVALID_MASK' : tsl2591_constant.AVALID_MASK
					}

special_funct = 		{ 'SetInterrupt' : tsl2591_constant.SetInterrupt,
						'ClearAlsInt' : tsl2591_constant.ClearAlsInt,
						'ClearAlsNoPersAlsInt' : tsl2591_constant.ClearAlsNoPersAlsInt,
						'ClearsNoPersAlsInt' : tsl2591_constant.ClearsNoPersAlsInt
					}

again_bit_list =	   { 'GAIN_LOW' : tsl2591_constant.GAIN_LOW,
					   'GAIN_MED' : tsl2591_constant.GAIN_MED,
					   'GAIN_HIGH' : tsl2591_constant.GAIN_HIGH,
					   'GAIN_MAX' : tsl2591_constant.GAIN_MAX
					}

again_byte_to_txt = 	{ tsl2591_constant.GAIN_LOW : 'GAIN_LOW' ,
					      tsl2591_constant.GAIN_MED : 'GAIN_MED',
					      tsl2591_constant.GAIN_HIGH : 'GAIN_HIGH',
					      tsl2591_constant.GAIN_MAX : 'GAIN_MAX'
					}

atime_bit_list =		{ 'TIME_100MS' : tsl2591_constant.TIME_100MS,
					    'TIME_200MS' : tsl2591_constant.TIME_200MS,
					    'TIME_300MS' : tsl2591_constant.TIME_300MS,
					    'TIME_400MS' : tsl2591_constant.TIME_400MS,
					    'TIME_500MS' : tsl2591_constant.TIME_500MS,
					    'TIME_600MS' : tsl2591_constant.TIME_600MS
					}

atime_byte_to_txt =		{ tsl2591_constant.TIME_100MS : 'TIME_100MS',
					      tsl2591_constant.TIME_200MS : 'TIME_200MS',
					      tsl2591_constant.TIME_300MS : 'TIME_300MS',
					      tsl2591_constant.TIME_400MS : 'TIME_400MS',
					      tsl2591_constant.TIME_500MS : 'TIME_500MS',
					      tsl2591_constant.TIME_600MS : 'TIME_600MS' 
					}

persist_bit_list = 		{ 'PERSIST_EVERY' : tsl2591_constant.PERSIST_EVERY,
						  'PERSIST_ANY'   : tsl2591_constant.PERSIST_ANY,
						  'PERSIST_2'	  : tsl2591_constant.PERSIST_2,
						  'PERSIST_3'	  : tsl2591_constant.PERSIST_3,
						  'PERSIST_5'	  : tsl2591_constant.PERSIST_5,
						  'PERSIST_10'	  : tsl2591_constant.PERSIST_10,
						  'PERSIST_15'	  : tsl2591_constant.PERSIST_15,
						  'PERSIST_20'	  : tsl2591_constant.PERSIST_20,
						  'PERSIST_25'	  : tsl2591_constant.PERSIST_25,
						  'PERSIST_30'	  : tsl2591_constant.PERSIST_30,
						  'PERSIST_35'	  : tsl2591_constant.PERSIST_35,
						  'PERSIST_40'	  : tsl2591_constant.PERSIST_40,
						  'PERSIST_45'	  : tsl2591_constant.PERSIST_45,
						  'PERSIST_50'	  : tsl2591_constant.PERSIST_50,
						  'PERSIST_55'	  : tsl2591_constant.PERSIST_55,
						  'PERSIST_60'	  : tsl2591_constant.PERSIST_60
						}

lux_const =				 { 'LUX_DF'          : tsl2591_constant.LUX_DF,
						   'LUX_COEFB'       : tsl2591_constant.LUX_COEFB,
						   'LUX_COEFC'       : tsl2591_constant.LUX_COEFC,
						   'LUX_COEFD'       : tsl2591_constant.LUX_COEFD,
						   'MAX_COUNT_100MS' : tsl2591_constant.MAX_COUNT_100MS,
						   'MAX_COUNT'       : tsl2591_constant.MAX_COUNT
						}

logger = logging.getLogger(__name__)

def conf_register_list() :

   tsl = TSL2591()
   tsl._logger = logging.getLogger('ecomet.tls2591.reglist') 
   reg_enable = {}
   reg_control = {}
   reg_als = {}
   reg_npers_als = {}
   reg_persist = {}
   reg_dev = {}
   reg_stat = {}
   channel = {}
   register = {}
   thr = {}
   
   enable = { 0x00: 'OFF',
              0x01: 'ON',
              0x02: 'ON',
              0x10: 'ON',
              0x40: 'ON',
              0x80: 'ON'
			}

   status = { 0x00 : 'OFF',
			   0x01 : 'ON',
			   0x08 : 'ON',
			   0x10 : 'ON'
			}

   again = { tsl2591_constant.GAIN_LOW : 'GAIN_LOW',
            tsl2591_constant.GAIN_MED : 'GAIN_MED',
            tsl2591_constant.GAIN_HIGH : 'GAIN_HIGH',
            tsl2591_constant.GAIN_MAX : 'GAIN_MAX'
			}

   atime = { tsl2591_constant.TIME_100MS : 'TIME_100MS',
			 tsl2591_constant.TIME_200MS : 'TIME_200MS',
			 tsl2591_constant.TIME_300MS : 'TIME_300MS',
			 tsl2591_constant.TIME_400MS : 'TIME_400MS',
			 tsl2591_constant.TIME_500MS : 'TIME_500MS',
			 tsl2591_constant.TIME_600MS :'TIME_600MS'
			}

   persist = { tsl2591_constant.PERSIST_EVERY : 'PERSIST_EVERY',
				tsl2591_constant.PERSIST_ANY : 'PERSIST_ANY',
				tsl2591_constant.PERSIST_2 : 'PERSIST_2',
				tsl2591_constant.PERSIST_3 : 'PERSIST_3',
				tsl2591_constant.PERSIST_5 : 'PERSIST_5',
				tsl2591_constant.PERSIST_10 : 'PERSIST_10',
				tsl2591_constant.PERSIST_15 : 'PERSIST_15',
				tsl2591_constant.PERSIST_20 :'PERSIST_20',
				tsl2591_constant.PERSIST_25 :'PERSIST_25',
				tsl2591_constant.PERSIST_30 : 'PERSIST_30',
				tsl2591_constant.PERSIST_35 : 'PERSIST_35',
				tsl2591_constant.PERSIST_40 : 'PERSIST_40',
				tsl2591_constant.PERSIST_45 : 'PERSIST_45',
				tsl2591_constant.PERSIST_50 : 'PERSIST_50',
				tsl2591_constant.PERSIST_55 : 'PERSIST_55',
				tsl2591_constant.PERSIST_60 : 'PERSIST_60'
				}

   reg_enable['NPIEN'] = enable[tsl.read_register( register = 'ENABLE' )[0] & enable_mask_list['ENABLE_NPIEN']]
   reg_enable['SAI'] = enable[tsl.read_register( register = 'ENABLE' )[0] & enable_mask_list['ENABLE_SAI']]
   reg_enable['AIEN'] = enable[tsl.read_register( register = 'ENABLE' )[0] & enable_mask_list['ENABLE_AIEN']]
   reg_enable['AEN'] = enable[tsl.read_register( register = 'ENABLE' )[0] & enable_mask_list['ENABLE_AEN']]
   reg_enable['POWER'] = enable[tsl.read_register( register = 'ENABLE' )[0] & enable_mask_list['ENABLE_POWER']]

   reg_control['RESET'] = enable[tsl.read_register( register = 'CONTROL' )[0] & ctrl_mask_list['CTLR_RESET']]
   reg_control['AGAIN'] = again[tsl.read_register( register = 'CONTROL' )[0] & ctrl_mask_list['CTLR_AGAIN']]
   reg_control['ATIME'] = atime[tsl.read_register( register = 'CONTROL' )[0] & ctrl_mask_list['CTLR_ATIME']]
   
   reg_persist['STATUS'] = persist[tsl.read_register( register = 'PERSIST_FILTER' )[0] & persist_mask_list['PERSIST']]
   reg_dev['PID'] = tsl.read_register( register = 'PACKAGE_PID' )[0] & pid_mask_list['PID']
   reg_dev['ID'] = tsl.read_register( register = 'DEVICE_ID' )[0] 
   
   reg_stat['NPINTR'] = status[tsl.read_register( register = 'STATUS' )[0] & status_mask_list['NPINTR_MASK']]
   reg_stat['AINT'] = status[tsl.read_register( register = 'STATUS' )[0] & status_mask_list['AINT_MASK']]
   reg_stat['AVALID'] = status[tsl.read_register( register = 'STATUS' )[0] & status_mask_list['AVALID_MASK']]
   
   channel['CHAN0'] = tsl.read_register( register = 'CHAN0' )[0]
   channel['CHAN1'] = tsl.read_register( register = 'CHAN1' )[0]

   thr['THR_AIL'] = hex(tsl.read_register( register = 'THR_AI_L' )[0])
   thr['THR_AIH'] = hex(tsl.read_register( register = 'THR_AI_H' )[0])
   thr['THR_NPAIL'] = hex(tsl.read_register( register = 'THR_NPAI_L' )[0])
   thr['THR_NPAIH'] = hex(tsl.read_register( register = 'THR_NPAI_H' )[0])

   register['ENABLE'] = reg_enable
   register['CONTROL'] = reg_control
   register['PERSIST'] = reg_persist
   register['DEVICE'] = reg_dev
   register['STATUS'] = reg_stat
   register['CHAN'] = channel
   register['THR'] = thr
   
   return (register);

class TSL2591(object):
    '''stl2591() RPM-Based  PWM  Fan  Controller'''

    def __init__(self, address=tsl2591_constant.TSL2591_ADDRESS, busnum=None, i2c=None, **kwargs) :
        '''Initialize the sn-gcja5.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self._gain = None
        self._IntegralTime = None

        self._id = self.read_register('DEVICE_ID')
        if(self._id[0] != 0x50):
           self._logger.fatal("ID = (%s)",hex(self._id[0]))
           return -1

        self.enable_ic
        self.set_gain('GAIN_MED')
        self.set_IntegralTime('TIME_200MS')
        self.write_register('PERSIST_FILTER',persist_bit_list['PERSIST_ANY'])
        self.disable_ic

    def self_test(self) :
        reg_status = 0
        ret = 0
        try :
          reg_status = self._device.readList(reg_list['STATE'],1)
        except :
          ret = 1
        if int.from_bytes(reg_status,"big") != 0 or ret != 0:
             ret = 2
        return ret
    @property
    def enable_ic(self) :
        ret = 0
        data = self.read_register('ENABLE')[0]
        data = data | enable_mask_list['ENABLE_POWER'] | enable_mask_list['ENABLE_AIEN'] | enable_mask_list['ENABLE_AEN'] | enable_mask_list['ENABLE_NPIEN']
        try:
           self.write_register('ENABLE',data)
        except :
           ret = ret + 1
        return (ret)
    @property
    def disable_ic(self) :
        ret = 0
        data = self.read_register('ENABLE')[0]
        data = data | enable_mask_list['DISABLE_POWER']
        try:
           self.write_register('ENABLE',data)
        except :
           ret = ret + 1
        return (ret)
    @property
    def reset_ic (self):
       print('Reset IC')
       control = self.read_register('CONTROL')[0]
       control |= ctrl_mask_list['CTLR_RESET']
       time.sleep(1)
       self.write_register('CONTROL',control)
    @property
    def get_gain (self):
       data = self.read_register('CONTROL')[0]
       return data & ctrl_mask_list['CTLR_AGAIN']
    def set_gain (self,data) :
       if data in ['GAIN_LOW','GAIN_MED','GAIN_HIGH','GAIN_MAX'] :
          control = self.read_register('CONTROL')[0]
          mask = ~ctrl_mask_list['CTLR_AGAIN']
          control &= mask
          control |= again_bit_list[data]
          self.write_register('CONTROL',control)
          self._gain = again_bit_list[data]
    @property
    def get_IntegralTime (self):
        data = self.read_register('CONTROL')[0]
        return data & ctrl_mask_list['CTLR_ATIME']
    def set_IntegralTime (self, data) :
        if data in ['TIME_100MS','TIME_200MS','TIME_300MS','TIME_400MS','TIME_500MS','TIME_600MS'] :
           control = self.read_register('CONTROL')[0]
           mask = ~ctrl_mask_list['CTLR_ATIME']
           control &= mask
           control |= atime_bit_list[data]
           self.write_register('CONTROL',control)
           self._IntegralTime = atime_bit_list[data]
    def read_register(self, register) :
        if register in ['ENABLE','CONTROL','STATUS','THR_AI_L','THR_AI_H','THR_NPAI_L','THR_NPAI_H',
			 'PERSIST_FILTER','PACKAGE_PID','DEVICE_ID','DEVICE_STATUS',
			 'CHAN0','CHAN1'] :
           ret = 0
           reg_status = -9999
           #print ( register )
           if register in ['THR_AI_L','THR_AI_H','THR_NPAI_L','THR_NPAI_H'] :
              try :
                 cregister = (reg_list['COMMAND'] | reg_list[register + 'TL']) & 0xff
                 reg_status = int(self._device.readU16(cregister))
              except :
                 ret = ret + 1
           elif register in ['CHAN0','CHAN1'] :	
              try :
                 cregister = (reg_list['COMMAND'] | reg_list[register + '_L']) & 0xff
                 reg_status = int(self._device.readU16(cregister))
                 #print("addr: ",hex(cregister)," data: ",hex(reg_status))
              except :
                 ret = ret + 1
           else :

              try :
                 cregister = (reg_list['COMMAND'] | reg_list[register]) & 0xff
                 reg_status = int(self._device.readU8(cregister))
              except :
                 ret = ret + 1
        return (reg_status,ret)
    def write_register(self, register,data) :
        if register in ['ENABLE','CONTROL','STATUS','THR_AI_L','THR_AI_H','THR_NPAI_L','THR_NPAI_H',
			 'PERSIST_FILTER'] :
           ret = 0
           #print ( register )
           if register in ['THR_AI_L','THR_AI_H','THR_NPAI_L','THR_NPAI_H'] :
              try :
                 cregister = (reg_list['COMMAND'] | reg_list[register + 'TL']) & 0xff
                 self._device.write16(cregister,data)
              except :
                 ret = ret + 1
           else :
              try :
                 cregister = (reg_list['COMMAND'] | reg_list[register]) & 0xff
                 self._device.write8(cregister,data)
              except :
                 ret = ret + 1
        return (ret)
    def Read_FullSpectrum(self, calibrate = None) :
       self.enable_ic
       if calibrate :
          data = (self.SelfCalibrate_perChannel('CHAN1')[0] << 16) | self.SelfCalibrate_perChannel('CHAN0')[0]
       else :
          data = (self.read_register('CHAN1')[0] << 16) | self.read_register('CHAN0')[0]
       self.disable_ic
       return (data,again_byte_to_txt[self._gain],atime_byte_to_txt[self._IntegralTime])
    def Read_Infrared(self, calibrate = None):
       self.enable_ic
       if calibrate :
          data = self.SelfCalibrate_perChannel('CHAN0')[0]
       else :
          data = self.read_register('CHAN0')[0]
       self.disable_ic
       return (data,again_byte_to_txt[self._gain],atime_byte_to_txt[self._IntegralTime])
    def Read_Visible(self, calibrate = None):
       if calibrate :
          ch1 = self.SelfCalibrate_perChannel('CHAN1')[0]
          ch0 = self.SelfCalibrate_perChannel('CHAN0')[0]
       else:
          ch1 = self.read_register('CHAN1')[0]
          ch0 = self.read_register('CHAN0')[0]
       self.disable_ic
       full = (ch1 << 16) | ch0
       return (full -ch1,again_byte_to_txt[self._gain],atime_byte_to_txt[self._IntegralTime])
    def SpecialFunction(self,funct):
       if funct in ['SetInterrupt','ClearAlsInt','ClearAlsNoPersAlsInt','ClearsNoPersAlsInt']:
          self.enable_ic
          cregister = (reg_list['COMMAND'] | special_funct[funct] & 0xff)
          self._device.write8(cregister,reg_list['STATUS'])
          self.disable_ic
    def Lux(self, calibrate = None):
       #print('start LUX ....')
       self.enable_ic
       #print('Measured Gain: ',again_byte_to_txt[self._gain])
       #print('Measured Time: ',atime_byte_to_txt[self._IntegralTime])
       for i in range(0, self._IntegralTime + 2):
          time.sleep(0.1)
       if calibrate == 1 :
           (channel_0,channel_1,ret) = self.SelfCalibrate
       else :
          channel_0 = self.read_register('CHAN0')[0]
          channel_1 = self.read_register('CHAN1')[0]
       #print('channel_0: ', channel_0)
       #print('cahnnel_1: ', channel_1)
       self.disable_ic

       self.SpecialFunction('ClearAlsNoPersAlsInt')

       atime = 100.0 * self._IntegralTime + 100.0

       if self._IntegralTime == atime_bit_list['TIME_100MS']:
          max_counts = lux_const['MAX_COUNT_100MS']
       else:
          max_counts = lux_const['MAX_COUNT']

       if channel_0 >= max_counts or channel_1 >= max_counts:
          gain_t = self.get_gain
          #print('Initial Gain: ',again_byte_to_txt[self._gain])
          if (gain_t != again_bit_list['GAIN_LOW']):
             gain_t = ((gain_t>>4)-1)<<4
             #print('Calculated Gain: {:02x}',again_byte_to_txt[self._gain])
             self.set_gain(gain_t)
             channel_0 = 0
             channel_1 = 0
             while( channel_0 <= 0 and channel_1 <=0 ):
                channel_0 = self.read_register('CHAN0')[0]
                channel_1 = self.read_register('CHAN1')[0]
                for i in range(0, self._IntegralTime + 2):
                   time.sleep(0.1)
          else :
             print('Numberical overflow!')
             raise RuntimeError('Numerical overflow!')
       again = 1.0
       if self._gain == again_bit_list['GAIN_MED']:
          again = 25.0
       elif self._gain == again_bit_list['GAIN_HIGH']:
          again = 428.0
       elif self._gain == again_bit_list['GAIN_MAX']:
          again = 9876.0

       #print('atime: ',atime)
       #print('again: ',again)
       #print('channel_0: ', channel_0)
       #print('cahnnel_1: ', channel_1)
       cpl = (atime * again) / lux_const['LUX_DF']
       lux1 = (channel_0 - (lux_const['LUX_COEFB'] * channel_1))/ cpl
       lux2 = ((lux_const['LUX_COEFC'] * channel_0) - (lux_const['LUX_COEFD'] * channel_1)) / cpl
       #print('cpl: ',cpl)
       #print('lux1: ',lux1)
       #print('lux2: ',lux2)

       return (max(int(lux1),int(lux2),int(0)),again_byte_to_txt[self._gain],atime_byte_to_txt[self._IntegralTime])
    @property
    def SelfCalibrate (self):
       self.set_gain('GAIN_MAX')
       self.set_IntegralTime('TIME_500MS')
       max_counts = lux_const['MAX_COUNT']
       for i in range(0, self._IntegralTime + 2):
          time.sleep(0.1)
       channel_0 = self.read_register('CHAN0')[0]
       channel_1 = self.read_register('CHAN1')[0]
       while ((channel_0 >= max_counts or channel_1 >= max_counts) and self.get_IntegralTime >= atime_bit_list['TIME_200MS'] and self.get_gain >= again_bit_list['GAIN_MED']):
          self._IntegralTime = self._IntegralTime - 1
          if self._IntegralTime == atime_bit_list['TIME_100MS']:
             max_counts = lux_const['MAX_COUNT_100MS']
          else:
             max_counts = lux_const['MAX_COUNT']
          self.set_IntegralTime(atime_byte_to_txt[self._IntegralTime])
          for i in range(0, self._IntegralTime + 2):
             time.sleep(0.1)
          channel_0 = self.read_register('CHAN0')[0]
          channel_1 = self.read_register('CHAN1')[0]
          if (channel_0 >= max_counts or channel_1 >= max_counts) :
             self._gain = ((self._gain>>4)-1)<<4
             self.set_gain(again_byte_to_txt[self._gain])
             for i in range(0, self._IntegralTime + 2):
                time.sleep(0.1)
             channel_0 = self.read_register('CHAN0')[0]
             channel_1 = self.read_register('CHAN1')[0]
             if (channel_0 < max_counts and channel_1 < max_counts) :
                #print('Calibrated Gain0: ',again_byte_to_txt[self._gain])
                #print('Calculated Time0: ',atime_byte_to_txt[self._IntegralTime])
                #print('channel_0: ', channel_0)
                #print('cahnnel_1: ', channel_1)
                return (channel_0,channel_1,0) # correctly set
          else :
             #print('Calibrated Gain1: ',again_byte_to_txt[self._gain])
             #print('Calculated Time1: ',atime_byte_to_txt[self._IntegralTime])
             #print('channel_0: ', channel_0)
             #print('cahnnel_1: ', channel_1)
             return (channel_0,channel_1,0) # correctly set
          #print('Gain,IT: ',channel_0,channel_1, max_counts,again_byte_to_txt[self.get_gain],atime_byte_to_txt[self.get_IntegralTime])

       if (channel_0 >= max_counts or channel_1 >= max_counts) :
          #print('Calibrated Gain2: ',again_byte_to_txt[self._gain])
          #print('Calculated Time2: ',atime_byte_to_txt[self._IntegralTime])
          #print('channel_0: ', channel_0)
          #print('cahnnel_1: ', channel_1)
          return (channel_0,channel_1,0) # correctly set
       self._IntegralTime = atime_bit_list['TIME_100MS']
       max_counts = lux_const['MAX_COUNT_100MS']
       self.set_IntegralTime('TIME_100MS')
       for i in range(0, self._IntegralTime + 2):
          time.sleep(0.1)
       channel_0 = self.read_register('CHAN0')[0]
       channel_1 = self.read_register('CHAN1')[0]
       if (channel_0 >= max_counts or channel_1 >= max_counts) :
          self._gain = again_bit_list['GAIN_LOW']
          self.set_gain('GAIN_LOW')
          for i in range(0, self._IntegralTime + 2):
             time.sleep(0.1)
          channel_0 = self.read_register('CHAN0')[0]
          channel_1 = self.read_register('CHAN1')[0]
          if (channel_0 >= max_counts or channel_1 >= max_counts) :
             raise RuntimeError('Numerical overflow!')
             return (lux_const['MAX_COUNT'],lux_const['MAX_COUNT'],1)
          else :
             #print('Calibrated Gain3: ',again_byte_to_txt[self._gain])
             #print('Calculated Time3: ',atime_byte_to_txt[self._IntegralTime])
             #print('channel_0: ', channel_0)
             #print('cahnnel_1: ', channel_1)
             return (channel_0,channel_1,0) # correctly set
       else :
          #print('Calibrated Gain4: ',again_byte_to_txt[self._gain])
          #print('Calculated Time4: ',atime_byte_to_txt[self._IntegralTime])
          #print('channel_0: ', channel_0)
          #print('cahnnel_1: ', channel_1)
          return (channel_0,channel_1,0) # correctly set
    def SelfCalibrate_perChannel (self,chan):
       self.set_gain('GAIN_MAX')
       self.set_IntegralTime('TIME_500MS')
       max_counts = lux_const['MAX_COUNT']
       for i in range(0, self._IntegralTime + 2):
          time.sleep(0.1)
       channel = self.read_register(chan)[0]
       while (channel >= max_counts and self.get_IntegralTime >= atime_bit_list['TIME_200MS'] and self.get_gain >= again_bit_list['GAIN_MED']):
          self._IntegralTime = self._IntegralTime - 1
          if self._IntegralTime == atime_bit_list['TIME_100MS']:
             max_counts = lux_const['MAX_COUNT_100MS']
          else:
             max_counts = lux_const['MAX_COUNT']
          self.set_IntegralTime(atime_byte_to_txt[self._IntegralTime])
          for i in range(0, self._IntegralTime + 2):
             time.sleep(0.1)
          channel = self.read_register(chan)[0]
          if (channel >= max_counts) :
             self._gain = ((self._gain>>4)-1)<<4
             self.set_gain(again_byte_to_txt[self._gain])
             for i in range(0, self._IntegralTime + 2):
                time.sleep(0.1)
             channel = self.read_register(chan)[0]
             if (channel < max_counts) :
                #print('Calibrated Gain0: ',again_byte_to_txt[self._gain])
                #print('Calculated Time0: ',atime_byte_to_txt[self._IntegralTime])
                #print('channel: ', channel)
                return (channel,0) # correctly set
          else :
             #print('Calibrated Gain1: ',again_byte_to_txt[self._gain])
             #print('Calculated Time1: ',atime_byte_to_txt[self._IntegralTime])
             #print('channel: ', channel)
             return (channel,0) # correctly set
          #print('Gain,IT: ',channel,max_counts,again_byte_to_txt[self.get_gain],atime_byte_to_txt[self.get_IntegralTime])

       if (channel < max_counts) :
          #print('Calibrated Gain0: ',again_byte_to_txt[self._gain])
          #print('Calculated Time0: ',atime_byte_to_txt[self._IntegralTime])
          #print('channel: ', channel)
          return (channel,0) # correctly set
       self._IntegralTime = atime_bit_list['TIME_100MS']
       max_counts = lux_const['MAX_COUNT_100MS']
       self.set_IntegralTime('TIME_100MS')
       for i in range(0, self._IntegralTime + 2):
          time.sleep(0.1)
       channel = self.read_register(chan)[0]
       if (channel >= max_counts) :
          self._gain = again_bit_list['GAIN_LOW']
          self.set_gain('GAIN_MED')
          for i in range(0, self._IntegralTime + 2):
             time.sleep(0.1)
          channel = self.read_register(chan)[0]
          if (channel >= max_counts) :
             raise RuntimeError('Numerical overflow!')
             return (lux_const['MAX_COUNT'],1)
          else :
             #print('Calibrated Gain2: ',again_byte_to_txt[self._gain])
             #print('Calculated Time2: ',atime_byte_to_txt[self._IntegralTime])
             #print('channel: ', channel)
             return (channel,0) # correctly set
       else :
          #print('Calibrated Gain3: ',again_byte_to_txt[self._gain])
          #print('Calculated Time3: ',atime_byte_to_txt[self._IntegralTime])
          #print('channel: ', channel)
          return (channel,0) # correctly set
    def SET_InterruptThreshold(self, HIGH, LOW):
        self.enable_ic
        self.write_register('THR_AI_L',LOW)
        self.write_register('THR_AI_H',HIGH)

        self.write_register('THR_NPAI_L',0x00)
        self.write_register('THR_NPAI_H',0xff)
        self.disable_ic
    def TSL2591_SET_LuxInterrupt(self, SET_LOW, SET_HIGH):
        atime  = 100 * self.IntegralTime + 100
        again = 1.0;
        if(self.Gain == MEDIUM_AGAIN):
            again = 25.0;
        elif(self.Gain == HIGH_AGAIN):
            again = 428.0
        elif(self.Gain == MAX_AGAIN):
            again = 9876.0;
        Cpl = (atime * again) / LUX_DF
        channel_1 = self.read_register('CHAN1')[0]

        SET_HIGH =  (int)(Cpl * SET_HIGH)+ 2*channel_1-1
        SET_LOW = (int)(Cpl * SET_LOW)+ 2*channel_1+1

        self.enable_ic
        self.write_register('THR_AI_L',SET_LOW)
        self.write_register('THR_AI_H',SET_HIGH)

        self.write_register('THR_NPAI_L',0x00)
        self.write_register('THR_NPAI_H',0xff)
        self.disable_ic
