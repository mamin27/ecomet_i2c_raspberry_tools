from __future__ import division
import logging
import time
import math
from ecomet_i2c_sensors.emc2301 import emc2301_constant
from ecomet_i2c_sensors.emc2301 import fan_type

fan_list = { 'POLES' : fan_type.POLES, 'EDGE' : fan_type.EDGE , 'MULTIPLIER' : fan_type.MULTIPLIER, 'FAN_TACH' : fan_type.FAN_TACH,
             'RANGE_500_1' : fan_type.RANGE_500_1, 'RANGE_1000_2' : fan_type.RANGE_1000_2, 'RANGE_2000_4' : fan_type.RANGE_2000_4, 'RANGE_4000_8' : fan_type.RANGE_4000_8,
             'EDGES_3_1POLE_05' : fan_type.EDGES_3_1POLE_05, 'EDGES_5_2POLE_1' : fan_type.EDGES_5_2POLE_1, 'EDGES_7_3POLE_15' : fan_type.EDGES_7_3POLE_15, 'EDGES_9_4POLE_2' : fan_type.EDGES_9_4POLE_2,
			 'UPDATE_100' : fan_type.UPDATE_100, 'UPDATE_200' : fan_type.UPDATE_200, 'UPDATE_300' : fan_type.UPDATE_300, 'UPDATE_400' : fan_type.UPDATE_400, 'UPDATE_500' : fan_type.UPDATE_500,
             'UPDATE_800' : fan_type.UPDATE_800, 'UPDATE_1200' : fan_type.UPDATE_1200, 'UPDATE_1600' : fan_type.UPDATE_1600,
             'DER_OPT_NO_DERIVATE' : fan_type.DER_OPT_NO_DERIVATE, 'DER_OPT_BASIC_DERIVATE' : fan_type.DER_OPT_BASIC_DERIVATE, 'DER_OPT_STEP_DERIVATE' : fan_type.DER_OPT_STEP_DERIVATE, 'DER_OPT_BOTH_DERIVATE' : fan_type.DER_OPT_BOTH_DERIVATE,
             'ERR_RNG_0RPM' : fan_type.ERR_RNG_0RPM, 'ERR_RNG_50RPM' : fan_type.ERR_RNG_50RPM, 'ERR_RNG_100RPM' : fan_type.ERR_RNG_100RPM, 'ERR_RNG_200RPM' : fan_type.ERR_RNG_200RPM,
             'GAIN_GAIND_1x' : fan_type.GAIN_GAIND_1x, 'GAIN_GAIND_2x' : fan_type.GAIN_GAIND_2x, 'GAIN_GAIND_4x' : fan_type.GAIN_GAIND_4x, 'GAIN_GAIND_8x' : fan_type.GAIN_GAIND_8x,
             'GAIN_GAINI_1x' : fan_type.GAIN_GAINI_1x, 'GAIN_GAINI_2x' : fan_type.GAIN_GAINI_2x, 'GAIN_GAINI_4x' : fan_type.GAIN_GAINI_4x, 'GAIN_GAINI_8x' : fan_type.GAIN_GAINI_8x,
             'GAIN_GAINP_1x' : fan_type.GAIN_GAINP_1x, 'GAIN_GAINP_2x' : fan_type.GAIN_GAINP_2x, 'GAIN_GAINP_4x' : fan_type.GAIN_GAINP_4x, 'GAIN_GAINP_8x' : fan_type.GAIN_GAINP_8x,
             'FAN_SPIN_UP_TIME1' : fan_type.FAN_SPIN_UP_TIME1, 'FAN_SPIN_UP_TIME2' : fan_type.FAN_SPIN_UP_TIME2, 'FAN_SPIN_UP_TIME3' : fan_type.FAN_SPIN_UP_TIME3, 'FAN_SPIN_UP_TIME4' : fan_type.FAN_SPIN_UP_TIME4,
             'FAN_SPIN_UP_SPIN' : fan_type.FAN_SPIN_UP_SPIN, 'FAN_SPIN_UP_NO_SPIN' : fan_type.FAN_SPIN_UP_NO_SPIN,
             'FAN_SPIN_UP_LVL1' : fan_type.FAN_SPIN_UP_LVL1, 'FAN_SPIN_UP_LVL2' : fan_type.FAN_SPIN_UP_LVL2, 'FAN_SPIN_UP_LVL3' : fan_type.FAN_SPIN_UP_LVL3, 'FAN_SPIN_UP_LVL4' : fan_type.FAN_SPIN_UP_LVL4,
             'FAN_SPIN_UP_LVL5' : fan_type.FAN_SPIN_UP_LVL5, 'FAN_SPIN_UP_LVL6' : fan_type.FAN_SPIN_UP_LVL6, 'FAN_SPIN_UP_LVL7' : fan_type.FAN_SPIN_UP_LVL7, 'FAN_SPIN_UP_LVL8' : fan_type.FAN_SPIN_UP_LVL8,
             'FAN_SPIN_UP_DF1' : fan_type.FAN_SPIN_UP_DF1, 'FAN_SPIN_UP_DF2' : fan_type.FAN_SPIN_UP_DF2, 'FAN_SPIN_UP_DF3' : fan_type.FAN_SPIN_UP_DF3, 'FAN_SPIN_UP_DF4' : fan_type.FAN_SPIN_UP_DF4,
             'FAN_PWM_BASE1' : fan_type.FAN_PWM_BASE1, 'FAN_PWM_BASE2' : fan_type.FAN_PWM_BASE2, 'FAN_PWM_BASE3' : fan_type.FAN_PWM_BASE3, 'FAN_PWM_BASE4' : fan_type.FAN_PWM_BASE4
           }

reg_list = { 'CONF' : emc2301_constant.CONF,'FAN_STAT' : emc2301_constant.FAN_STAT, 'FAN_STALL' :  emc2301_constant.FAN_STALL, 'FAN_SPIN' : emc2301_constant.FAN_SPIN,
             'DRIVE_FALL' : emc2301_constant.DRIVE_FALL, 'FAN_INTERRUPT' : emc2301_constant.FAN_INTERRUPT, 
             'PWM_POLARITY' : emc2301_constant.PWM_POLARITY, 'PWM_OUTPUT' :  emc2301_constant.PWM_OUTPUT, 'PWM_BASE' : emc2301_constant.PWM_BASE, 
             'FAN_SETTING' : emc2301_constant.FAN_SETTING, 'PWM_DIVIDE' : emc2301_constant.PWM_DIVIDE, 
             'FAN_CONF1' : emc2301_constant.FAN_CONF1, 'FAN_CONF2' : emc2301_constant.FAN_CONF2, 'GAIN' : emc2301_constant.GAIN,
             'FAN_SPIN_UP' : emc2301_constant.FAN_SPIN_UP, 'FAN_MAX_STEP' : emc2301_constant.FAN_MAX_STEP, 'FAN_MIN_DRIVE' :  emc2301_constant.FAN_MIN_DRIVE,
             'TACH_COUNT' : emc2301_constant.TACH_COUNT, 'FAN_FAIL_BAND_LB' : emc2301_constant.FAN_FAIL_BAND_LB, 'FAN_FAIL_BAND_HB' :   emc2301_constant.FAN_FAIL_BAND_HB,
             'FAN_FAIL_BAND' : emc2301_constant.FAN_FAIL_BAND, 'TACH_TARGET' : emc2301_constant.TACH_TARGET,
             'TACH_TARGET_LB' : emc2301_constant.TACH_TARGET_LB, 'TACH_TARGET_HB' :  emc2301_constant.TACH_TARGET_HB, 
             'TACH_READ' : emc2301_constant.TACH_READ, 'TACH_READ_HB' : emc2301_constant.TACH_READ_HB, 'TACH_READ_LB' : emc2301_constant.TACH_READ_LB,
             'SOFTWARE_LOCK' : emc2301_constant.SOFTWARE_LOCK, 'PRODUCT_ID' : emc2301_constant.PRODUCT_ID, 'MANUF_ID' : emc2301_constant.MANUF_ID, 'REVISION_ID' : emc2301_constant.REVISION_ID
        }
conf_bit_list =    { 'MASK' :  emc2301_constant.MASK,
                     'DIS_TO' : emc2301_constant.DIS_TO,
                     'WD_EN' :  emc2301_constant.WD_EN,
                     'DR_EXT_CLK' :  emc2301_constant.DR_EXT_CLK,
                     'USE_EXT_CLK' : emc2301_constant.USE_EXT_CLK,
                     'MASK_M' : emc2301_constant.MASK_M,
                     'DIS_TO_M' : emc2301_constant.DIS_TO_M,
                     'WD_EN_M' :  emc2301_constant.WD_EN_M,
                     'DR_EXT_CLK_M' :  emc2301_constant.DR_EXT_CLK_M,
                     'USE_EXT_CLK_M' : emc2301_constant.USE_EXT_CLK_M
                }
                      
fan_stat_bit_list = { 'WATCH' :  emc2301_constant.WATCH,
                      'DRIVE_FAIL' : emc2301_constant.DRIVE_FAIL,
                      'DRIVE_FAIL_I' : emc2301_constant.DRIVE_FAIL_I,
                      'FAN_SPIN' :  emc2301_constant.FAN_SPIN,
                      'FAN_STALL' :  emc2301_constant.FAN_STALL,
                      'FAN_INT_EN' : emc2301_constant.FAN_INT_EN,
                      'WATCH_M' : emc2301_constant.WATCH_M,
                      'DRIVE_FAIL_M' : emc2301_constant.DRIVE_FAIL_M,
                      'DRIVE_FAIL_I_M' : emc2301_constant.DRIVE_FAIL_I_M,
                      'FAN_SPIN_M' :  emc2301_constant.FAN_SPIN_M,
                      'FAN_STALL_M' :  emc2301_constant.FAN_STALL_M,
                      'FAN_INT_EN_M' : emc2301_constant.FAN_INT_EN_M
                }

conf1_bit_list =     { 'EN_ALGO' :  emc2301_constant.EN_ALGO, 
                       'RANGE' : emc2301_constant.RANGE,
                       'EDGES' : emc2301_constant.EDGES,
                       'UPDATE' : emc2301_constant.UPDATE,
                       'EN_ALGO_M' : emc2301_constant.EN_ALGO_M,
                       'RANGE_M' : emc2301_constant.RANGE_M,
                       'EDGES_M' : emc2301_constant.EDGES_M,
                       'UPDATE_M' : emc2301_constant.UPDATE_M
                       }

conf2_bit_list = { 'ERR_RNG' : emc2301_constant.ERR_RNG,
                        'DER_OPT' : emc2301_constant.DER_OPT,
                        'GLITCH_EN' : emc2301_constant.GLITCH_EN,
                        'EN_RRC' : emc2301_constant.EN_RRC,
                        'ERR_RNG_M' : emc2301_constant.ERR_RNG_M,
                        'DER_OPT_M' : emc2301_constant.DER_OPT_M,
                        'GLITCH_EN_M' : emc2301_constant.GLITCH_EN_M,
                        'EN_RRC_M' : emc2301_constant.EN_RRC_M
					  }
					  
gain_bit_list = { 'GAIND' : emc2301_constant.GAIND,
                  'GAINI' : emc2301_constant.GAINI,
                  'GAINP' : emc2301_constant.GAINP,
                  'GAIND_M' : emc2301_constant.GAIND_M,
                  'GAINI_M' : emc2301_constant.GAINI_M,
                  'GAINP_M' : emc2301_constant.GAINP_M
					  }

spin_bit_list =          { 'FAN_SPIN_UP_TIME' : emc2301_constant.FAN_SPIN_UP_TIME,
                           'FAN_SPIN_UP_LVL' : emc2301_constant.FAN_SPIN_UP_LVL,
                           'FAN_SPIN_UP_NOKICK' : emc2301_constant.FAN_SPIN_UP_NOKICK,
                           'FAN_SPIN_UP_DRIVE_FAIL_CNT' : emc2301_constant.FAN_SPIN_UP_DRIVE_FAIL_CNT,
                           'FAN_SPIN_UP_TIME_M' : emc2301_constant.FAN_SPIN_UP_TIME_M,
                           'FAN_SPIN_UP_LVL_M' : emc2301_constant.FAN_SPIN_UP_LVL_M,
                           'FAN_SPIN_UP_NOKICK_M' : emc2301_constant.FAN_SPIN_UP_NOKICK_M,
                           'FAN_SPIN_UP_DRIVE_FAIL_CNT_M' : emc2301_constant.FAN_SPIN_UP_DRIVE_FAIL_CNT_M
                         }

pwm_bit_list =      { 'FAN_INT_EN' : emc2301_constant.FAN_INT_EN,
                      'POLARITY' : emc2301_constant.POLARITY,
                      'PWM_OT' : emc2301_constant.PWM_OT,
                      'BASE' :  emc2301_constant.BASE,
                      'FAN_INT_EN_M' : emc2301_constant.FAN_INT_EN_M,
                      'POLARITY_M' : emc2301_constant.POLARITY_M,
                      'PWM_OT_M' : emc2301_constant.PWM_OT_M,
                      'BASE_M' :  emc2301_constant.BASE_M
                    }
                    
lock_bit_list = { 'LOCK' : emc2301_constant.LOCK,
                  'LOCK_M' : emc2301_constant.LOCK_M
                }
                    
list_4096 = [32,64,128,256,512,1024,2048,4096]
list_128 = [1,2,4,8,16,32,64,128]
list_32 = [1,2,4,8,16,32]
list_16 = [0,0,0,1,2,4,8,16]
                     
logger = logging.getLogger(__name__)

def word_lb (nm) :

   list_lb = [16,8,4,2,1]
   list_sum = [128,64,32,16,8]

   sum = 0
   tmp = nm
   sum_lb = 0
   for idx in range (0,5) :
     if tmp >= list_lb[idx] :
       sum_lb = sum_lb + list_sum[idx]
       tmp = tmp - list_lb[idx]  
     
   return (sum_lb)

def conf_register_list() :

   emc = EMC2301()
   emc._logger = logging.getLogger('ecomet.emc2301.reglist') 
   register = {}
   reg_conf = {}
   reg_spin_up = {}
   reg_fan_stat = {}
   reg_pwm = {}
   reg_tach = {}
   reg_id = {}
   
   emc_drv_fail_cnt = { 0: 'DISABLE',
                        64: '16UP_PER',
                        128: '32UP_PER' ,
                        192: '64UP_PER'
						}

   emc_spin_lvl = { 0: '30%',
                    4: '35%',
                    8: '40%',
                    12: '45%',
                    16: '50%',
                    20: '55%',
                    24: '60%',
                    28: '65%'
					}

   emc_spin_time = { 0: '250ms',
                     1: '500ms',
                     2: '1s',
                     3: '2s'
                    }
                    
   emc_range = {  0:  '500>1',
	              32: '1000>2',
			      64: '2000>4',
				  96: '4000>8'
               }

   emc_edges =  {  0:  '3>1POLE>0.5',
	               8:  '5>2POLE>1',
	     	      16: '7>3POLE>1.5',
				  24: '9>4POLE>2'
               }
               
   emc_update =  {  0:  '100ms',
	                1:  '200ms',
	     	        2:  '300ms',
				    3:  '400ms',
				    4:  '500ms',
				    5:  '800ms',
				    6:  '1200ms',
				    7:  '1600ms'
               }
               
   emc_der_opt =  {  0:  'NO_DERIVATE',
	                 8:  'BASIC_DERIVATE',
	     	        16: 'STEP_DERIVATE',
				    24: 'BOTH_DERIVATE'
               }
               
   emc_err_rng =  {  0: '0RPM',
	                 2: '50RPM',
	     	         4: '100RPM',
				     6: '200RPM'
               }
               
   emc_gainp =  {    0: '1x',
	                 1: '2x',
	     	         2: '4x',
				     3: '8x'
               }
               
   emc_gaini =  {    0: '1x',
	                 4: '2x',
	     	         8: '4x',
				     12: '8x'
               }
               
   emc_gaind =  {    0: '1x',
	                 16: '2x',
	     	         32: '4x',
				     48: '8x'
               }
               
   emc_base =  {    0: '26.00kHz',
	                 1: '19.531kHz',
	     	         2: '4.882Hz',
				     3: '2.441Hz'
               }
                      
   reg_conf['MASK'] = 'MASKED' if emc.read_register( register = 'CONF' )[0] & conf_bit_list['MASK'] > 0 else 'UNMASKED'
   reg_conf['DIS_TO'] = 'DISABLED' if emc.read_register( register = 'CONF' )[0] & conf_bit_list['DIS_TO'] > 0 else 'ENABLED'
   reg_conf['WD_EN'] = 'OPERATE' if emc.read_register( register = 'CONF' )[0] & conf_bit_list['WD_EN'] > 0 else 'DISABLED'
   reg_conf['DR_EXT_CLK'] = 'CLK_OUTPUT' if emc.read_register( register = 'CONF' )[0] & conf_bit_list['DR_EXT_CLK'] > 0 else 'CLK_INPUT'
   reg_conf['USE_EXT_CLK'] = 'EXTERNAL' if emc.read_register( register = 'CONF' )[0] & conf_bit_list['USE_EXT_CLK'] > 0 else 'INTERNAL'
   reg_conf['EN_ALGO'] = 'ENABLED' if emc.read_register( register = 'FAN_CONF1' )[0] & conf1_bit_list['EN_ALGO'] > 0 else 'DISABLED'
   reg_conf['RANGE'] = emc_range.get((emc.read_register( register = 'FAN_CONF1' )[0] & conf1_bit_list['RANGE']))
   reg_conf['EDGES'] = emc_edges.get((emc.read_register( register = 'FAN_CONF1' )[0] & conf1_bit_list['EDGES']))
   reg_conf['UPDATE'] = emc_update.get((emc.read_register( register = 'FAN_CONF1' )[0] & conf1_bit_list['UPDATE']))
   reg_conf['EN_RRC'] = 'ENABLED' if emc.read_register( register = 'FAN_CONF2' )[0] & conf2_bit_list['EN_RRC'] > 0 else 'DISABLED'
   reg_conf['GLITCH_EN'] = 'ENABLED' if emc.read_register( register = 'FAN_CONF2' )[0] & conf2_bit_list['GLITCH_EN'] > 0 else 'DISABLED'
   reg_conf['DER_OPT'] = emc_der_opt.get((emc.read_register( register = 'FAN_CONF2' )[0] & conf2_bit_list['DER_OPT']))
   reg_conf['ERR_RNG'] = emc_err_rng.get((emc.read_register( register = 'FAN_CONF2' )[0] & conf2_bit_list['ERR_RNG']))
   reg_conf['GAIND'] = emc_gaind.get((emc.read_register( register = 'GAIN' )[0] & gain_bit_list['GAIND']))
   reg_conf['GAINI'] = emc_gaini.get((emc.read_register( register = 'GAIN' )[0] & gain_bit_list['GAINI']))
   reg_conf['GAINP'] = emc_gainp.get((emc.read_register( register = 'GAIN' )[0] & gain_bit_list['GAINP']))
   
   reg_spin_up['FAN_SPIN_UP_DRIVE_FAIL_CNT'] = emc_drv_fail_cnt.get((emc.read_register( register = 'FAN_SPIN_UP' )[0] & spin_bit_list['FAN_SPIN_UP_DRIVE_FAIL_CNT']))
   reg_spin_up['FAN_SPIN_UP_NOKICK'] = 'NO_SPIN' if emc.read_register( register = 'FAN_SPIN_UP' )[0] & spin_bit_list['FAN_SPIN_UP_NOKICK'] > 0 else 'SPIN'
   reg_spin_up['FAN_SPIN_UP_LVL'] = emc_spin_lvl.get((emc.read_register( register = 'FAN_SPIN_UP' )[0] & spin_bit_list['FAN_SPIN_UP_LVL']))
   reg_spin_up['FAN_SPIN_UP_TIME'] = emc_spin_time.get((emc.read_register( register = 'FAN_SPIN_UP' )[0] & spin_bit_list['FAN_SPIN_UP_TIME']))
   tbin = emc.read_register( register = 'FAN_MAX_STEP' )[0]
   res = 0
   for idx in range (0,6) :
     res = res + (tbin % 2)  * list_32[idx]
     tbin = tbin >> 1
   reg_spin_up['FAN_MAX_STEP'] = res
   tbin = emc.read_register( register = 'FAN_MIN_DRIVE' )[0]
   res = 0
   for idx in range (0,8) :
     res = res + (tbin % 2)  * list_128[idx]
     tbin = tbin >> 1
   reg_spin_up['FAN_MIN_DRIVE'] = round((res/255)*100,1)
   
   reg_fan_stat['WATCH'] = 'EXPIRED' if emc.read_register( register = 'FAN_STAT' )[0] & fan_stat_bit_list['WATCH'] > 0 else 'NOT_SET'
   reg_fan_stat['DRIVE_FAIL'] = 'CANOT_REACH' if emc.read_register( register = 'FAN_STAT' )[0] & fan_stat_bit_list['DRIVE_FAIL'] > 0 else 'REACH'
   reg_fan_stat['FAN_SPIN'] = 'CANOT_SPIN' if emc.read_register( register = 'FAN_STAT' )[0] & fan_stat_bit_list['FAN_SPIN'] > 0 else 'SPIN'
   reg_fan_stat['FAN_STALL'] = 'STALL' if emc.read_register( register = 'FAN_STAT' )[0] & fan_stat_bit_list['FAN_STALL'] > 0 else 'NOT_STALL'
   reg_fan_stat['FAN_INT'] = 'ALERT' if emc.read_register( register = 'FAN_INTERRUPT' )[0] & fan_stat_bit_list['FAN_INT_EN'] > 0 else 'NO_ALERT'
   tbin = emc.read_register( register = 'FAN_SETTING' )[0]
   #emc._logger.info(tbin)
   res = 0
   for idx in range (0,8) :
     res = res + (tbin % 2) * list_128[idx]  
     tbin = tbin >> 1
   reg_fan_stat['FAN_SETTING'] = round((res/255)*100,2)
   
   
   reg_pwm['PWM_POLARITY'] = 'INVERTED' if emc.read_register( register = 'PWM_POLARITY' )[0] & pwm_bit_list['POLARITY'] > 0 else 'NORMAL'
   reg_pwm['PWM_OUTPUT'] = 'PUSH-PULL' if emc.read_register( register = 'PWM_OUTPUT' )[0] & pwm_bit_list['PWM_OT'] > 0 else 'OPEN-DRAIN'
   reg_pwm['PWM_BASE'] = emc_base.get((emc.read_register( register = 'PWM_BASE' )[0] & pwm_bit_list['BASE']))
   tbin = emc.read_register( register = 'PWM_DIVIDE' )[0]
   res = 0
   for idx in range (0,8) :
     res = res + (tbin % 2)  * list_128[idx]
     tbin = tbin >> 1
   reg_pwm['PWM_DIVIDE'] = res

   tbin = emc.read_register( register = 'TACH_COUNT' )[0]
   res = 0
   for idx in range (0,8) :
     res = res + (tbin % 2) * list_4096[idx]
     tbin = tbin >> 1
   reg_tach['TACH_COUNT'] = res 
   tbin_lb = emc.read_register( register = 'FAN_FAIL_BAND_LB' )[0]
   tbin_hb = emc.read_register( register = 'FAN_FAIL_BAND_HB' )[0]
   res = 0
   for idx in range (0,8) :
     res = res + (tbin_hb % 2) * list_4096[idx]
     tbin_hb = tbin_hb >> 1
   for idx in range (0,8) :
     res = res + (tbin_lb % 2) * list_16[idx]
     tbin_lb = tbin_lb >> 1
   reg_tach['FAN_FAIL_BAND'] = res
   tbin_lb = emc.read_register( register = 'TACH_TARGET_LB' )[0]
   tbin_hb = emc.read_register( register = 'TACH_TARGET_HB' )[0]
   res = 0
   for idx in range (0,8) :
     res = res + (tbin_hb % 2) * list_4096[idx]
     tbin_hb = tbin_hb >> 1
   for idx in range (0,8) :
     res = res + (tbin_lb % 2) * list_16[idx]
     tbin_lb = tbin_lb >> 1
   reg_tach['TACH_TARGET'] = res
   (tbin_hb,tbin_lb,ret) = emc.read_register( register = 'TACH_READ' )
   res = 0
   for idx in range (0,8) :
     res = res + (tbin_hb % 2) * list_4096[idx]
     tbin_hb = tbin_hb >> 1
   for idx in range (0,8) :
     res = res + (tbin_lb % 2) * list_16[idx]
     tbin_lb = tbin_lb >> 1
   reg_tach['TACH_READ'] = res
       
   reg_id['PRODUCT_ID'] = emc.productid()[0]
   reg_id['MANUF_ID'] = emc.manufid()[0]
   reg_id['REVISION_ID'] = emc.revisionid()[0]
   
   register['CONF'] = reg_conf
   register['FAN_STAT'] = reg_fan_stat
   register['SPIN'] = reg_spin_up
   register['PWM'] = reg_pwm
   register['TACH'] = reg_tach
   register['ID'] = reg_id
   
   register['LOCK'] = 'LOCKED' if emc.read_register( register = 'SOFTWARE_LOCK' )[0] & lock_bit_list['LOCK'] > 0 else 'UNLOCKED'
   
   return (register);

class EMC2301(object):
    '''emc2301() RPM-Based  PWM  Fan  Controller'''

    def __init__(self, address=emc2301_constant.EMC2301_ADDRESS, busnum=emc2301_constant.I2CBUS, i2c=None, **kwargs) :
        '''Initialize the emc2301.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
    def self_test(self) :
        try :
          (np,ret) = self.productid()
        except :
          ret = 1
        return ret
    def read_register(self, register) :
        if register in ['CONF','FAN_STAT','PWM_DIVIDE','FAN_SETTING','FAN_CONF1','FAN_CONF2',
                        'FAN_SPIN','DRIVE_FALL','FAN_INTERRUPT',
                        'GAIN', 'FAN_SPIN_UP', 'FAN_MAX_STEP','FAN_MIN_DRIVE',
                        'PWM_POLARITY','PWM_OUTPUT','PWM_BASE',
                        'TACH_COUNT','FAN_FAIL_BAND_LB','FAN_FAIL_BAND_HB','TACH_TARGET_LB','TACH_TARGET_HB','TACH_READ_LB','TACH_READ_HB',
                        'PRODUCT_ID','MANUF_ID','REVISION_ID','SOFTWARE_LOCK'] :
           ret = 0
           reg_type = 1
           try :
              reg_status_bita = self._device.readList(reg_list[register],1)
              if not reg_status_bita:
                return (0x00,2)
              reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[0])
              reg_status = int(reg_status_hex, 0)
           except :
              ret = ret + 1
        elif register in ['TACH_READ'] :
           ret = 0
           reg_type = 2
           try :
              reg_status_bita = self._device.readList(reg_list[register],2)
              self._logger.debug('step3')
           except :
              ret = ret + 1
        if ret > 0 :
           self._logger.debug('read_register %s failed (%s)',register,ret)
           if reg_type == 1 :
             return (0x00,ret)
           elif reg_type == 2 :
             return (0x00,0x00,ret)
        else :
           if reg_type == 1 :
             self._logger.debug('read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
             self._logger.debug('read_register %s, data: %s', register, '{0:b}'.format(reg_status))
             return (reg_status,0)
           elif reg_type == 2 :
             self._logger.debug('lo_byte %s, hi_byte %s', '{0:02x}'.format(reg_status_bita[1]), '{0:02x}'.format(reg_status_bita[0]))
             reg_status_hex = '0x' + '{0:02x}'.format(reg_status_bita[1]) + '{0:02x}'.format(reg_status_bita[0])
             self._logger.debug('2 bytes read_register, init reg_status: %s', '{0}'.format(reg_status_hex))
             return (reg_status_bita[1],reg_status_bita[0],ret)
    def write_register(self, register, bits = None, bit = None, value = None) :
          ret = 0
          if register in ['CONF','FAN_CONF1','FAN_CONF2','FAN_SPIN_UP','GAIN',
                          'FAN_INTERRUPT','PWM_POLARITY','PWM_OUTPUT','PWM_BASE','SOFTWARE_LOCK'] :
            (reg_status,ret) = self.read_register( register = register )
            for ibit in bits :
               if '_CLR' not in ibit :
                  bit_mask = ibit + '_M'
               else :
                  bit_mask = ibit[:-4] + '_M'
               if register == 'CONF' :
                  reg_status = reg_status & conf_bit_list[bit_mask]
                  if '_CLR' not in ibit :
                    reg_status = reg_status | conf_bit_list[ibit]
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
               if register in ['SOFTWARE_LOCK'] :
                  reg_status = reg_status & lock_bit_list[bit_mask]
                  if '_CLR' not in ibit :
                    reg_status = reg_status | lock_bit_list[ibit]
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
               if register in ['FAN_CONF1'] :
                  if ibit in ['RANGE'] :
                    reg_status = reg_status & conf1_bit_list[bit_mask] | (bit << 5)
                  elif ibit in ['EDGES'] :
                    reg_status = reg_status & conf1_bit_list[bit_mask] | (bit << 3)
                  elif ibit in ['UPDATE'] :
                    reg_status = reg_status & conf1_bit_list[bit_mask] | (bit << 0)
                  else :	  
                    reg_status = reg_status & conf1_bit_list[bit_mask]
                    if '_CLR' not in ibit :
                       reg_status = reg_status | conf1_bit_list[ibit]
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
               if register in ['FAN_CONF2'] :
                  if ibit in ['DER_OPT'] :
                    reg_status = reg_status & conf2_bit_list[bit_mask] | (bit << 3)
                  elif ibit in ['ERR_RNG'] :	
                    reg_status = reg_status & conf2_bit_list[bit_mask] | (bit << 1)
                  else :
                    reg_status = reg_status & conf2_bit_list[bit_mask]
                    if '_CLR' not in ibit :
                       reg_status = reg_status | conf2_bit_list[ibit]
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
               if register in ['GAIN'] :
                  if ibit in ['GAINP'] :
                    reg_status = reg_status & gain_bit_list[bit_mask] | (bit << 0)
                  elif ibit in ['GAINI'] :
                    reg_status = reg_status & gain_bit_list[bit_mask] | (bit << 2)
                  elif ibit in ['GAIND'] :
                    reg_status = reg_status & gain_bit_list[bit_mask] | (bit << 4) 	
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
               if register in ['FAN_SPIN_UP'] :
                  if ibit in ['FAN_SPIN_UP_TIME'] :
                    reg_status = reg_status & spin_bit_list[bit_mask] | (bit << 0)
                  elif ibit in ['FAN_SPIN_UP_LVL'] :
                    reg_status = reg_status & spin_bit_list[bit_mask] | (bit << 2)
                  elif ibit in ['FAN_SPIN_UP_NOKICK'] :
                    reg_status = reg_status & spin_bit_list[bit_mask] | (bit << 5)
                  elif ibit in ['FAN_SPIN_UP_DRIVE_FAIL_CNT'] :
                    reg_status = reg_status & spin_bit_list[bit_mask] | (bit << 6)
                  else:
                    reg_status = reg_status & spin_bit_list[bit_mask]                    
                    if '_CLR' not in ibit :
                       reg_status = reg_status | spin_bit_list[ibit]
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
               if register in ['FAN_INTERRUPT','PWM_POLARITY','PWM_OUTPUT','PWM_BASE'] :
                  if ibit in ['BASE'] :
                    reg_status = reg_status & pwm_bit_list[bit_mask] | (bit << 0)
                  else:
                    reg_status = reg_status & pwm_bit_list[bit_mask]                    
                    if '_CLR' not in ibit :
                       reg_status = reg_status | pwm_bit_list[ibit]
                  self._logger.debug('write_register, init reg_status: %s, bit %s', '{0:02X}'.format(reg_status), format(ibit))
            reg_status = reg_status & 0xff
            try :
               self._device.write8(reg_list[register],reg_status)
            except :
               ret = ret + 1
               self._logger.debug('writelist error')
          elif register in ['FAN_SETTING','FAN_MAX_STEP','FAN_MIN_DRIVE','PWM_DIVIDE'] :
            if register in ['FAN_SETTING','FAN_MIN_DRIVE','PWM_DIVIDE'] :
              if value <= 255 :
                reg_status = value
              elif register in ['FAN_MIN_DRIVE'] :
                reg_status = 102 #default value for FAM_MIN_DRIVE
              elif register in ['PWM_DIVIDE'] :
                reg_status = 1 #default value for PWM_DIVIDE
              elif register in ['FAN_SETTING'] :
                reg_status = 100 #default set to 0
            if register in ['FAN_MAX_STEP'] :
              if value <= 63 :
                list_lb = [32,16,8,4,2,1]
                list_sum = [32,16,8,4,2,1]

                sum = 0
                tmp = value
                sum_lb = 0
                for idx in range (0,6) :
                  if tmp >= list_lb[idx] :
                    sum = sum + list_lb[idx]
                    sum_lb = sum_lb + list_sum[idx]
                    tmp = tmp - sum
                reg_status = sum_lb
              else :
                reg_status = 16 #default for FAN_MAX_STEP
            self._logger.debug('write_register %s, final_reg_status: (%s)', register,'{0:02X}'.format(reg_status))
            try :
              self._device.write8(reg_list[register],reg_status)
            except :
              ret = ret + 1
          elif register in ['TACH_TARGET','FAN_FAIL_BAND'] :
            if value <= 31 :
               sum_lb = word_lb (value)
               self._logger.debug('write_register %s, final_sum_lb: (%s)', register,'{0:02X}'.format(sum_lb))
               try :
                 self._device.write8(reg_list[register],sum_lb)
                 self._device.write8(reg_list[register]+1,0)
               except :
                 ret = ret + 1
            else :
               list_hb = [4096,2048,1024,512,256,128,64,32]
               list_sum = [128,64,32,16,8,4,2,1]	

               sum = 0
               tmp = value
               sum_hb = 0
               for idx in range (0,8) :
                 if tmp >= list_hb[idx] :
                   sum_hb = sum_hb + list_sum[idx]
                   tmp = tmp - list_hb[idx]              
               sum_lb = word_lb (tmp)
               self._logger.debug('write_register %s, final_sum_lb: (%s)', register, '{0:02X}'.format(sum_lb))
               self._logger.debug('write_register %s, final_sum_hb: (%s)', register,'{0:02X}'.format(sum_hb))
               try :
                 self._device.write8(reg_list[register],sum_lb)
                 self._device.write8(reg_list[register]+1,sum_hb)
               except :
                 ret = ret + 1
          elif register in ['TACH_COUNT'] :
            list_hb = [4096,2048,1024,512,256,128,64,32]
            list_sum = [128,64,32,16,8,4,2,1]
            
            sum = 0
            tmp = value
            sum_hb = 0
            for idx in range (0,8) :
              if tmp >= list_hb[idx] :
                sum_hb = sum_hb + list_sum[idx]
                tmp = tmp - list_hb[idx]               
            self._logger.debug('write_register %s, final_sum_hb: (%s)', register,'{0:02X}'.format(sum_hb))
            try :
              self._device.write8(reg_list[register],sum_hb)
            except :
              ret = ret + 1
              self._logger.debug('write_register %s, writelist error', register)
          else :
              ret = 1
          if ret > 1 :
             self._logger.debug('write_register %s failed (%s)', register, ret)
          return ret
    def speed (self) :
       (tbin_lb,tbin_hb,ret) = self.read_register( register = 'TACH_READ' )
       res = 0
       for idx in range (0,8) :
         res = res + (tbin_hb % 2) * list_4096[idx]
         tbin_hb = tbin_hb >> 1
       for idx in range (0,8) :
         res = res + (tbin_lb % 2) * list_16[idx]
         tbin_lb = tbin_lb >> 1
       self._logger.debug('speed byte %s ', res)
       if res == 0 :
         out = 0
       else :
         out = int(1/fan_list['POLES'] * ((fan_list['EDGE'] - 1)/(res * 1/fan_list['MULTIPLIER'])) * fan_list['FAN_TACH'] * 60)
       return (out,ret)
    def fan_kick_up (self,offset,interval,sum_sample,new_value,time_offset = None) :
       sample = [0] * (sum_sample)
       time = [0] * (sum_sample)
       if time_offset == None :
         time_init = 0
       else :
         time_init = time_offset
       from time import sleep
       sleep(offset)
       self._logger.info('kick up fan to {}'.format(new_value))
       self.write_register(register = 'FAN_SETTING', value = new_value)
       for index in range (0,sum_sample) :
         res = 0
         sleep(interval)
         time_init = time_init + interval
         (tbin_lb,tbin_hb,ret) = self.read_register( register = 'TACH_READ' )
         for idx in range (0,8) :
           res = res + (tbin_hb % 2) * list_4096[idx]
           tbin_hb = tbin_hb >> 1
         for idx in range (0,8) :
           res = res + (tbin_lb % 2) * list_16[idx]
           tbin_lb = tbin_lb >> 1
         if res != 0 :
           time[index] = round(time_init,3)
           sample[index] = int(1/fan_list['POLES'] * ((fan_list['EDGE'] - 1)/(res * 1/fan_list['MULTIPLIER'])) * fan_list['FAN_TACH'] * 60)
       return (sample,time)
    def productid (self) :
       ret = 0
       (temp,lret) = self.read_register( register = 'PRODUCT_ID' )
       if lret > 0 :
          ret = ret + 1
       if ret > 0 : 
           self._logger.error('Read error %s'.format(ret))
           return (0,ret)
       else :
           self._logger.debug('PRODUCT_ID: %s','{0:02X}'.format(temp))
           return ('{0:02X}'.format(temp),0)
    def manufid (self) :
       ret = 0
       (temp,lret) = self.read_register( register = 'MANUF_ID' )
       if lret > 0 :
          ret = ret + 1
       if ret > 0 : 
           self._logger.error('Read error %s'.format(ret))
           return (0,ret)
       else :
           self._logger.debug('MANUF_ID: %s','{0:02X}'.format(temp))
           return ('{0:02X}'.format(temp),0)
    def revisionid (self) :
       ret = 0
       (temp,lret) = self.read_register( register = 'REVISION_ID' )
       if lret > 0 :
          ret = ret + 1
       if ret > 0 : 
           self._logger.error('Read error %s'.format(ret))
           return (0,ret)
       else :
           self._logger.debug('REVISION_ID: %s','{0:02X}'.format(temp))
           return ('{0:02X}'.format(temp),0)
