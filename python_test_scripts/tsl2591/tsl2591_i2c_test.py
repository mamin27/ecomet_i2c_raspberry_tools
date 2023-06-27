#!/usr/bin/env python3

import sys,os
sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  tsl2591 import tsl2591,tsl2591_constant
#from  ecomet_i2c_sensors.tsl2591 import tsl2591
import logging

sens = tsl2591.TSL2591()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='tsl2591.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.tsl2591')
sens._logger.info('Start logging ...')

#print(tsl2591.conf_register_list())
#print('enable ic')
#sens.enable_ic()
#print(tsl2591.conf_register_list())
#sens.disable_ic()
#print(tsl2591.conf_register_list())

#sens.write_register('THR_AI',117835020)
#sens.write_register('THR_NPAI',185207049)
#sens.reset_ic()

#print('Gain: ',sens.get_gain())
#print('IntegralTime: ',sens.get_IntegralTime())

#sens.set_gain('GAIN_MED')
#print(tsl2591.conf_register_list())
#sens.set_IntegralTime('TIME_200MS')
#print(tsl2591.conf_register_list())
#ret = sens.SelfCalibrate
#print ('SelfCalibration ret = ',ret)

data = sens.Read_FullSpectrum
data2 = sens.Read_Infrared
data3 = sens.Read_Visible
lux = sens.Lux(calibrate = 1)

print('Lux: ',lux)
print('Infrared light: ', data2)
print('Visible light: ',data3)
print('Full spectrum (IR + visible) light: ',data)
