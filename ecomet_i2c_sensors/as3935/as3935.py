'''!
  @origin code
  @file DFRobot_AS3935_Lib.py
  @brief Define the basic structure of the DFRobot_AS3935 class, the implementation of the basic methods.
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author      TangJie(jie.tamg@dfrobot.com)
  @version  V1.0.2
  @date  2021-9-28
  @url https://github.com/DFRobot/DFRobot_AS3935
  
  Updated Code: 2024-03-13
  Copyright (c) 2024 eComet Co.Ltd (https://twitter.com/mminar7)
  @author      <mminar7@gmail.com>
  @license	   GPL-3.0
'''
from time import sleep
import logging
from ecomet_i2c_sensors.as3935 import as3935_constant

reg_list = { 'POWER_REG' : as3935_constant.POWER_REG, 'DISTANCE_REG' : as3935_constant.DISTANCE_REG, 'SET_IRQ_SIGNAL' : as3935_constant.SET_IRQ_SIGNAL,
             'STAT_REG_1' : as3935_constant.STAT_REG_1, 'STAT_REG_2' : as3935_constant.STAT_REG_2, 'STAT_REG_3' : as3935_constant.STAT_REG_3,
             'PRESET_DEFAULT' : as3935_constant.PRESET_DEFAULT, 'CALIB_RCO' : as3935_constant.CALIB_RCO,
             'ENG_LIGHT_MMSB' : as3935_constant.ENG_LIGHT_MMSB, 'ENG_LIGHT_LB' : as3935_constant.ENG_LIGHT_LB, 'ENG_LIGHT_HB' : as3935_constant.ENG_LIGHT_HB
        }

class AS3935:
   def __init__(self, address=as3935_constant.AS3935_I2C_ADDR3, busnum=None, i2c=None, **kwargs) :
        '''Initialize the as3935.'''
        # Setup I2C interface for the device.
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self._logger = logging.getLogger(__name__)    
#        self._device = i2c.get_i2c_device(address, busnum, **kwargs)   
        self._device = i2c.get_i2c_device(address, busnum=busnum, i2c_interface='smbus2', **kwargs)


#    @brief Configure sensor 
#    @param capacitance Antenna tuning capcitance (must be integer multiple of 8, 8 - 120 pf)
#    @param location    Indoor/outdoor mode selection
#    @param disturber   Enable/disable disturber detection

   def manual_cal(self, capacitance, location, disturber):
     self.powerUp()
     if location == 1:
       self.setIndoors()
     else:
       self.setOutdoors()

     if disturber == 0:
       self.disturberDis()
     else:
       self.disturberEn()

     self.setIrqOutputSource(0)
     sleep(0.5)
     self.setTuningCaps(capacitance)

   def set_tuning_caps(self, capVal):
       #Assume only numbers divisible by 8 (because that's all the chip supports)
       flags = as3935_constant.SET_IRQ_SIGNAL_FLAGS()
       (flags.asbyte,ret) = self.read_register('SET_IRQ_SIGNAL')
       if capVal > 120: #cap_value out of range, assume highest capacitance
           flags.tun_cap = 0b1111		#set capacitance bits to maximum
       else:
           flags.tun_cap = capVal >> 3  #set capacitance bits
       self.write_register('SET_IRQ_SIGNAL', flags.asbyte)
       reg_stat,ret = self.read_register('SET_IRQ_SIGNAL')
       self._logger.debug('capacitance set to 8x%d'%(reg_stat & 0x0F))

   def power_up(self):
     flags = as3935_constant.POWER_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('POWER_REG')
     flags.power = as3935_constant.POWER_REG_FLAGS.power_up
     self.write_register('POWER_REG', flags.asbyte)
     self._logger.debug('Power up')
     flags = as3935_constant.SET_IRQ_SIGNAL_FLAGS()
     (flags.asbyte,ret) = self.read_register('SET_IRQ_SIGNAL')
     flags.disp_srco = 1
     self.write_register('SET_IRQ_SIGNAL', flags.asbyte)
     self.cal_RCO() #run RCO cal cmd
     sleep(0.002)
     (flags.asbyte,ret) = self.read_register('SET_IRQ_SIGNAL')
     flags.disp_srco = 0
     self.write_register('SET_IRQ_SIGNAL', flags.asbyte)

   def power_down(self):
     #register 0x00, PWD bit: 0 (sets PWD)
     flags = as3935_constant.POWER_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('POWER_REG')
     flags.power = as3935_constant.POWER_REG_FLAGS.power_down
     self.write_register('POWER_REG', flags.asbyte)
     self._logger.debug('Power down')

   def cal_RCO(self):
     flags = as3935_constant.CALIB_RCO_FLAGS()
     err = self.write_register('CALIB_RCO', flags.calib_cmd)
     sleep(0.002) #wait 2ms to complete
     return err

   def set_indoors(self):
     flags = as3935_constant.POWER_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('POWER_REG')
     flags.afe_gb = 0b10010
     err = self.write_register('POWER_REG', flags.asbyte)
     sleep(0.002) #wait 2ms to complete
     self._logger.info("Set to indoors model")
     return err

   def set_outdoors(self):
     flags = as3935_constant.POWER_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('POWER_REG')
     flags.afe_gb = 0b01110
     err = self.write_register('POWER_REG', flags.asbyte)
     sleep(0.002) #wait 2ms to complete
     self._logger.info("Set to outdoors model")
     return err

   def disturber_dis(self):
     flags = as3935_constant.STAT_REG_3_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_3')
     flags.mask_dist = 1
     self.write_register('STAT_REG_3', flags.asbyte)
     self._logger.info("Disenable disturber detection")

   def disturber_en(self):
     flags = as3935_constant.STAT_REG_3_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_3')
     flags.mask_dist = 0
     self.write_register('STAT_REG_3', flags.asbyte)
     self._logger.info("Enable disturber detection")

   def get_interrupt_src(self):
     #0 = unknown src, 1 = lightning detected, 2 = disturber, 3 = Noise level too high
     sleep(0.03) #wait 3ms before reading (min 2ms per pg 22 of datasheet)
     flags = as3935_constant.STAT_REG_3_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_3')
     if flags.int == as3935_constant.STAT_REG_3_FLAGS.int_l:
       return 1 #lightning caused interrupt
     elif flags.int == as3935_constant.STAT_REG_3_FLAGS.int_d:
       return 2 #disturber detected
     elif flags.int == as3935_constant.STAT_REG_3_FLAGS.int_nh:
       return 3 #Noise level too high
     else:
       return 0 #interrupt result not expected

   @property
   def reset(self):
     flags = as3935_constant.PRESET_DEFAULT_FLAGS()
     err = self.write_register('PRESET_DEFAULT', flags.reset_cmd)
     sleep(0.002) #wait 2ms to complete
     return err

#    Sets LCO_FDIV register
#    @param fdiv Set 0, 1, 2 or 3 for ratios of 16, 32, 64 and 128, respectively
   def set_lco_fdiv(self,fdiv):
     flags = as3935_constant.STAT_REG_3_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_3')
     self.write_register('STAT_REG_3',(flags.lco_fdiv & 0x03) << 6)

   def set_irq_output_source(self, irqSelect):
     #set interrupt source - what to display on IRQ pin
     flags = as3935_constant.SET_IRQ_SIGNAL_FLAGS()
     (flags.asbyte,ret) = self.read_register('SET_IRQ_SIGNAL')
     flags.disp_lco = 0
     flags.disp_srco = 0
     flags.disp_trco = 0
     if irqSelect == 1:
       flags.disp_trco = 1	#set only TRCO bit 
     elif irqSelect == 2:
       flags.disp_srco = 1	#set only SRCO bit
     elif irqSelect == 3:
       flags.disp_lco = 0	#set only LCO bit
     self.write_register('SET_IRQ_SIGNAL', flags.asbyte)

   def get_lightning_distKm(self):
     flags = as3935_constant.DISTANCE_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('DISTANCE_REG')
     if flags.distance == as3935_constant.DISTANCE_REG_FLAGS.dist_out :
        return 99
     else :
        return flags.distance

   def get_strike_energy_raw(self):
     flags = as3935_constant.ENG_LIGHT_MMSB_FLAGS()
     (flags.asbyte,ret) = self.read_register('ENG_LIGHT_MMSB')
     nrgyRaw = (flags.s_lig_mm) << 16
     flags = as3935_constant.ENG_LIGHT_HB_FLAGS()
     (flags.asbyte,ret) = self.read_register('ENG_LIGHT_HB')
     nrgyRaw |= (flags.s_lig_hb << 8)
     flags = as3935_constant.ENG_LIGHT_LB_FLAGS()
     (flags.asbyte,ret) = self.read_register('ENG_LIGHT_LB')
     nrgyRaw |= (flags.s_lig_lb)
     self._logger.debug('nrgy: %06x'%nrgyRaw)
        
     return nrgyRaw/16777

   def set_min_strikes(self, minStrk):
     #This function sets min strikes to the closest available number, rounding to the floor,
     #where necessary, then returns the physical value that was set. Options are 1, 5, 9 or 16 strikes.
     flags = as3935_constant.STAT_REG_2_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_2')
     if minStrk < 5:
       flags.minv_num_light = as3935_constant.STAT_REG_2_FLAGS.min_num_light_0
       self.write_register('STAT_REG_2', flags.asbyte)
       return 1
     elif minStrk < 9:
       flags.minv_num_light = as3935_constant.STAT_REG_2_FLAGS.min_num_light_1
       self.write_register('STAT_REG_2', flags.asbyte)
       return 5
     elif minStrk < 16:
       flags.minv_num_light = as3935_constant.STAT_REG_2_FLAGS.min_num_light_2
       self.write_register('STAT_REG_2', flags.asbyte)
       return 9
     else:
       flags.minv_num_light = as3935_constant.STAT_REG_2_FLAGS.min_num_light_3
       self.write_register('STAT_REG_2', flags.asbyte)
       return 16

   def clear_statistics(self):
     #clear is accomplished by toggling CL_STAT bit 'high-low-high' (then set low to move on)
     flags = as3935_constant.STAT_REG_2_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_2')
     flags.cl_stat = as3935_constant.STAT_REG_2_FLAGS.stat_high  #high
     self.write_register('STAT_REG_2', flags.asbyte)
     flags.cl_stat = as3935_constant.STAT_REG_2_FLAGS.stat_low   #low
     self.write_register('STAT_REG_2', flags.asbyte)
     flags.cl_stat = as3935_constant.STAT_REG_2_FLAGS.stat_high  #high
     self.write_register('STAT_REG_2', flags.asbyte)

#    @return 0~7
   def get_noise_floor_lv1(self):
     flags = as3935_constant.STAT_REG_1_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_1')
     return flags.nf_lev   #should return value from 0-7, see table 16 for info

   def set_noise_floor_lv1(self, nfSel):
     flags = as3935_constant.STAT_REG_1_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_1')
     if nfSel <= 7:
        flags.nf_lev = nfSel
     else:							#out of range, set to default (power-up value 010)
        flags.nf_lev = as3935_constant.STAT_REG_1_FLAGS.nfl_in_2
     self.write_register('STAT_REG_1', flags.asbyte)
   
   def get_watchdog_threshold(self):
     #This function is used to read WDTH. It is used to increase robustness to disturbers,
     #though will make detection less efficient (see page 19, Fig 20 of datasheet)
     #default value of 0010
     #values should only be between 0x00 and 0x0F (0 and 7)
     flags = as3935_constant.STAT_REG_1_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_1')
     return flags.wdth   #should return value from 0-7, see table 16 for info

   def set_watchdog_threshold(self, wdth_lvl):
     flags = as3935_constant.STAT_REG_1_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_1')
     if wdth_lvl <= 10:
        flags.wdth = wdth_lvl
     else:							#out of range, set to default
        flags.wdth = as3935_constant.STAT_REG_1_FLAGS.wdth_2
     self.write_register('STAT_REG_1', flags.asbyte)

   def get_spike_rejection(self):
     #This function is used to read SREJ (spike rejection). Similar to the Watchdog threshold,
     #it is used to make the system more robust to disturbers, though will make general detection
     #less efficient (see page 20-21, especially Fig 21 of datasheet)
     #default value of 0010
     #values should only be between 0x00 and 0x0F (0 and 7)
     flags = as3935_constant.STAT_REG_2_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_2')
     return flags.srej 

   def set_spike_rejection(self, srej_lvl):
     flags = as3935_constant.STAT_REG_2_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_2')
     if srej_lvl <= 15:
        flags.srej = srej_lvl
     else:							#out of range, set to default
        flags.srej = as3935_constant.STAT_REG_2_FLAGS.srej_2
     self.write_register('STAT_REG_2', flags.asbyte)
        
   def print_all_regs(self):
     flags = as3935_constant.POWER_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('POWER_REG')
     self._logger.info('Reg 0x00: %02x'%flags.asbyte)
     flags = as3935_constant.STAT_REG_1_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_1')
     self._logger.info('Reg 0x01: %02x'%flags.asbyte)
     flags = as3935_constant.STAT_REG_2_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_2')
     self._logger.info('Reg 0x02: %02x'%flags.asbyte)
     flags = as3935_constant.STAT_REG_3_FLAGS()
     (flags.asbyte,ret) = self.read_register('STAT_REG_3')
     self._logger.info('Reg 0x03: %02x'%flags.asbyte)
     self._logger.info('Reg STRIKE_ENERGY: %s'%str(self.get_strike_energy_raw()))
     flags = as3935_constant.DISTANCE_REG_FLAGS()
     (flags.asbyte,ret) = self.read_register('DISTANCE_REG')
     self._logger.info('Reg 0x07: %02x'%flags.asbyte)
     flags = as3935_constant.SET_IRQ_SIGNAL_FLAGS()
     (flags.asbyte,ret) = self.read_register('SET_IRQ_SIGNAL')
     self._logger.info('Reg 0x08: %02x'%flags.asbyte)

   def read_register(self, register) :
       reg_status = -9999
       ret = 0
       if register in ['POWER_REG','STAT_REG_1','STAT_REG_2','STAT_REG_3','DISTANCE_REG','SET_IRQ_SIGNAL','ENG_LIGHT_LB','ENG_LIGHT_HB', 'ENG_LIGHT_MMSB'] :
          try :
             reg_status = self._device.readU8(reg_list[register])
          except :
             ret = ret + 1
       return(reg_status,ret)

   def write_register(self, register,data) :
       ret = 0
       #print ( register )
       if register in ['POWER_REG','STAT_REG_1','STAT_REG_2','STAT_REG_3','SET_IRQ_SIGNAL','PRESET_DEFAULT','CALIB_RCO'] :
          self._device.write8(reg_list[register],data)
          try :
             self._device.write8(reg_list[register],data)
          except :
             ret = ret + 1
       return (ret)
