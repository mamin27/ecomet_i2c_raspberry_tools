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
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

sens = tsl2591.TSL2591()
sens._logger = logging.getLogger('ecomet.tsl2591')
sens._logger.info('Start logging ...')

#sens.reset_ic  make throuble

sens._logger.info('Manual Setting of Gain and Integral Time.')
sens._logger.info('<--------------------------------------->')

data = sens.Read_FullSpectrum ()
data2 = sens.Read_Infrared ()
data3 = sens.Read_Visible ()
lux = sens.Lux()

sens._logger.info('Lux: (%s)',lux[0])
sens._logger.info('Infrared light: (%s)', data2[0])
sens._logger.info('Visible light: (%s)',data3[0])
sens._logger.info('Full spectrum (IR + visible) light: (%s)',data[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',lux[1],lux[2])

sens.reset_ic
sens.set_gain('GAIN_MED')
sens.set_IntegralTime('TIME_300MS')

data = sens.Read_FullSpectrum ()
data2 = sens.Read_Infrared ()
data3 = sens.Read_Visible ()
lux = sens.Lux()

sens._logger.info('Lux: (%s)',lux[0])
sens._logger.info('Infrared light: (%s)', data2[0])
sens._logger.info('Visible light: (%s) ',data3[0])
sens._logger.info('Full spectrum (IR + visible) light: (%s)',data[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',lux[1],lux[2])

sens.reset_ic
sens.set_gain('GAIN_HIGH')
sens.set_IntegralTime('TIME_500MS')

data = sens.Read_FullSpectrum ()
data2 = sens.Read_Infrared ()
data3 = sens.Read_Visible ()
lux = sens.Lux()

sens._logger.info('Lux: (%s)',lux[0])
sens._logger.info('Infrared light: (%s)', data2[0])
sens._logger.info('Visible light: (%s)',data3[0])
sens._logger.info('Full spectrum (IR + visible) light: (%s)',data[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',lux[1],lux[2])

sens.reset_ic
sens._logger.info('Calibration')
sens._logger.info('<--------------------------------------->')

lux = sens.Lux(calibrate = 1)
data = sens.Read_FullSpectrum (calibrate = 1)
data2 = sens.Read_Infrared (calibrate = 1)
data3 = sens.Read_Visible (calibrate = 1)

sens._logger.info('Lux: (%s)',lux[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',lux[1],lux[2])
sens._logger.info('Infrared light: (%s)', data2[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',data2[1],data2[2])
sens._logger.info('Visible light: (%s)',data3[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',data3[1],data3[2])
sens._logger.info('Full spectrum (IR + visible) light: (%s)',data[0])
sens._logger.info('Measure Gain: (%s) IntegralTime: (%s)',data[1],data[2])

sens._logger.info('Set Interrupt')
sens._logger.info('<--------------------------------------->')
sens.SET_InterruptThreshold(HIGH = 0xff00, LOW = 0x0010)
sens._logger.info('List of Registers')
sens._logger.info('<--------------------------------------->')
sens._logger.info (tsl2591.conf_register_list())
