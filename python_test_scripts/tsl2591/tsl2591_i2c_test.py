#!/usr/bin/env python3

import sys,os
sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  tsl2591 import tsl2591,tsl2591_constant
#from  ecomet_i2c_sensors.tsl2591 import tsl2591
import logging

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

sens = tsl2591.TSL2591()
sens._logger = logging.getLogger('ecomet.tsl2591')
sens._logger.info('Start logging ...')

#sens.reset_ic  make throuble

print('Manual Setting of Gain and Integral Time.')

data = sens.Read_FullSpectrum ()
data2 = sens.Read_Infrared ()
data3 = sens.Read_Visible ()
lux = sens.Lux()

print('Lux: ',lux[0])
print('Infrared light: ', data2[0])
print('Visible light: ',data3[0])
print('Full spectrum (IR + visible) light: ',data[0])
print('Measure Gain: ',lux[1],' IntegralTime: ',lux[2])

sens.set_gain('GAIN_MED')
sens.set_IntegralTime('TIME_300MS')

data = sens.Read_FullSpectrum ()
data2 = sens.Read_Infrared ()
data3 = sens.Read_Visible ()
lux = sens.Lux()

print('Lux: ',lux[0])
print('Infrared light: ', data2[0])
print('Visible light: ',data3[0])
print('Full spectrum (IR + visible) light: ',data[0])
print('Measure Gain: ',lux[1],' IntegralTime: ',lux[2])

sens.set_gain('GAIN_HIGH')
sens.set_IntegralTime('TIME_500MS')

data = sens.Read_FullSpectrum ()
data2 = sens.Read_Infrared ()
data3 = sens.Read_Visible ()
lux = sens.Lux()

print('Lux: ',lux[0])
print('Infrared light: ', data2[0])
print('Visible light: ',data3[0])
print('Full spectrum (IR + visible) light: ',data[0])
print('Measure Gain: ',lux[1],' IntegralTime: ',lux[2])

print('Calibration')

lux = sens.Lux(calibrate = 1)
data = sens.Read_FullSpectrum (calibrate = 1)
data2 = sens.Read_Infrared (calibrate = 1)
data3 = sens.Read_Visible (calibrate = 1)

print('Lux: ',lux[0])
print('Measure Gain: ',lux[1],' IntegralTime: ',lux[2])
print('Infrared light: ', data2[0])
print('Measure Gain: ',data2[1],' IntegralTime: ',data2[2])
print('Visible light: ',data3[0])
print('Measure Gain: ',data3[1],' IntegralTime: ',data3[2])
print('Full spectrum (IR + visible) light: ',data[0])
print('Measure Gain: ',data[1],' IntegralTime: ',data[2])
