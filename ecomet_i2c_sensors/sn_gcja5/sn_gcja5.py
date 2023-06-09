from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.sn_gcja5 import sn_gcja5_constant

reg_list = { 'PM1_0_LL' : sn_gcja5_constant.PM1_0_LL,'PM1_0_LH' : sn_gcja5_constant.PM1_0_LH, 'PM1_0_HL' :  sn_gcja5_constant.PM1_0_HL, 'PM1_0_HH' : sn_gcja5_constant.PM1_0_HH,
			 'PM2_5_LL' : sn_gcja5_constant.PM2_5_LL,'PM2_5_LH' : sn_gcja5_constant.PM2_5_LH, 'PM2_5_HL' :  sn_gcja5_constant.PM2_5_HL, 'PM2_5_HH' : sn_gcja5_constant.PM2_5_HH,
			 'PM10_LL' : sn_gcja5_constant.PM10_LL,'PM10_LH' : sn_gcja5_constant.PM10_LH, 'PM10_HL' :  sn_gcja5_constant.PM10_HL, 'PM10_HH' : sn_gcja5_constant.PM10_HH,
			 'P0_5_L' : sn_gcja5_constant.P0_5_L,'P0_5_H' : sn_gcja5_constant.P0_5_H,
			 'P1_L' : sn_gcja5_constant.P1_L,'P1_H' : sn_gcja5_constant.P1_H,
			 'P2_5_L' : sn_gcja5_constant.P2_5_L,'P2_5_H' : sn_gcja5_constant.P2_5_H,
			 'P5_L' : sn_gcja5_constant.P5_L,'P5_H' : sn_gcja5_constant.P5_H,
			 'P7_5_L' : sn_gcja5_constant.P7_5_L,'P7_5_H' : sn_gcja5_constant.P7_5_H,
			 'P10_L' : sn_gcja5_constant.P10_L,'P10_H' : sn_gcja5_constant.P10_H,
             'STATE' : sn_gcja5_constant.STATE
        }
state_mask_list =    { 'SENSOR_STAT' :  sn_gcja5_constant.SENSOR_STAT,
                     'PD_STAT' : sn_gcja5_constant.PD_STAT,
                     'LD_STAT' :  sn_gcja5_constant.LD_STAT,
                     'FAN_STAT' :  sn_gcja5_constant.FAN_STAT
                }
                      
sensor_stat_bit_list = { 'NULL' :  sn_gcja5_constant.NULL,
                      'ANY1' : sn_gcja5_constant.ANY1,
                      'ANY2' : sn_gcja5_constant.ANY2,
                      'ANY3' :  sn_gcja5_constant.ANY3
                }

pd_stat_bit_list =     { 'PD_NORMAL' :  sn_gcja5_constant.PD_NORMAL, 
                       'PD_NORMAL_COR' : sn_gcja5_constant.PD_NORMAL_COR,
                       'PD_ABNORM' : sn_gcja5_constant.PD_ABNORM,
                       'PD_ABNORM_COR' : sn_gcja5_constant.PD_ABNORM_COR
                       }

ld_stat_bit_list = { 'LD_NORMAL' :  sn_gcja5_constant.LD_NORMAL, 
                       'LD_NORMAL_COR' : sn_gcja5_constant.LD_NORMAL_COR,
                       'LD_ABNORM' : sn_gcja5_constant.LD_ABNORM,
                       'LD_ABNORM_COR' : sn_gcja5_constant.LD_ABNORM_COR
					  }
					  
fan_stat_bit_list = { 'FAN_NORMAL' : sn_gcja5_constant.FAN_NORMAL,
                  'FAN_NORMAL_COR' : sn_gcja5_constant.FAN_NORMAL_COR,
                  'FAN_CALIB' : sn_gcja5_constant.FAN_CALIB,
                  'FAN_ABNORM' : sn_gcja5_constant.FAN_ABNORM
					  }
                     
logger = logging.getLogger(__name__)

def conf_register_list() :

   gcj = SN_GCJA5()
   gcj._logger = logging.getLogger('ecomet.sn-gcja5.reglist') 
   reg_mass = {}
   reg_particle = {}
   reg_part_perc = {}
   reg_stat = {}
   register = {}
   
   status = { 0: 'NONE',
              1: 'ANY1',
              2: 'ANY2' ,
              3: 'ANY3'
						}

   pd_status = { 0: 'NORMAL',
                 1: 'NORMAL_COR',
                 2: 'ABNORM',
                 3: 'ABNORM_COR'
					}

   ld_status = { 0: 'NORMAL',
                 1: 'NORMAL_COR',
                 2: 'ABNORM',
                 3: 'ABNORM_COR'
                    }
                    
   fan_status = {  0:  'NORMAL',
	               1: 'NORMAL_COR',
			       2: 'CALIB',
				   3: 'ABNORM'
               }

   reg_mass['PM1_0'] = gcj.read_register( register = 'PM1_0' )[0]
   reg_mass['PM2_5'] = gcj.read_register( register = 'PM2_5' )[0]
   reg_mass['PM10'] = gcj.read_register( register = 'PM10' )[0]

   reg_particle['P0_5'] = gcj.read_register( register = 'P0_5' )[0]
   reg_particle['P1'] = gcj.read_register( register = 'P1' )[0]
   reg_particle['P2_5'] = gcj.read_register( register = 'P2_5' )[0]
   reg_particle['P5'] = gcj.read_register( register = 'P5' )[0]
   reg_particle['P7_5'] = gcj.read_register( register = 'P7_5' )[0]
   reg_particle['P10'] = gcj.read_register( register = 'P10' )[0]

   sum = reg_particle['P0_5'] + reg_particle['P1'] + reg_particle['P2_5'] + reg_particle['P5'] + reg_particle['P7_5'] + reg_particle['P10']
   reg_part_perc['P0.5'] = round(reg_particle['P0_5']/sum * 100,1)
   reg_part_perc['P1'] = round(reg_particle['P1']/sum * 100,1)
   reg_part_perc['P2_5'] = round(reg_particle['P2_5']/sum * 100,1)
   reg_part_perc['P5'] = round(reg_particle['P5']/sum * 100,1)
   reg_part_perc['P7_5'] = round(reg_particle['P7_5']/sum * 100,1)
   reg_part_perc['P10'] = round(reg_particle['P10']/sum * 100,1)

   data = gcj.read_register( register = 'STATE' )[0]
   reg_stat['STAT'] = status.get((data & state_mask_list['SENSOR_STAT']))
   reg_stat['PD'] = pd_status.get((data & state_mask_list['PD_STAT']))
   reg_stat['LD'] = ld_status.get((data & state_mask_list['LD_STAT']))
   reg_stat['FAN'] = fan_status.get((data & state_mask_list['FAN_STAT']))

   register['MASS'] = reg_mass
   register['PARTICLE'] = reg_particle
   register['PART_PERC'] = reg_part_perc
   register['STATUS'] = reg_stat
   
   return (register);

class SN_GCJA5(object):
    '''sn-gcja5() RPM-Based  PWM  Fan  Controller'''

    def __init__(self, address=sn_gcja5_constant.SN_GCJA5_ADDRESS, busnum=None, i2c=None, **kwargs) :
        '''Initialize the sn-gcja5.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
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
    def read_register(self, register) :
        if register in ['PM1_0','PM2_5','PM10',
                        'P0_5','P1','P2_5','P5','P7_5','P10',
                        'STATE'] :
           ret = 0
           reg_status = -9999
           #print ( register )
           if register in ['PM1_0','PM2_5','PM10'] :
              try :
                 reg_status_ll = self._device.readList(reg_list[register + '_LL'],1)
                 reg_status_lh = self._device.readList(reg_list[register + '_LH'],1)
                 reg_status_hl = self._device.readList(reg_list[register + '_HL'],1)
                 reg_status_hh = self._device.readList(reg_list[register + '_HH'],1)
                 reg_status_list = bytes(reg_status_hh) + bytes(reg_status_hl) + bytes(reg_status_lh) + bytes(reg_status_ll)
                 reg_status = int.from_bytes(reg_status_list,"big")
                 reg_status = reg_status/1000
              except :
                 ret = ret + 1
           elif register in ['P0_5','P1','P2_5','P5','P7_5','P10'] :
              try :
                 reg_status_l = self._device.readList(reg_list[register + '_L'],1)
                 reg_status_h = self._device.readList(reg_list[register + '_H'],1)
                 reg_status_list = bytes(reg_status_h) + bytes(reg_status_l)
                 reg_status = int.from_bytes(reg_status_list,"big")
              except :
                 ret = ret + 1
           else :

              try :
                 reg_status = int.from_bytes(self._device.readList(reg_list[register],1),"big")
              except :
                 ret = ret + 1
        return (reg_status,ret)

