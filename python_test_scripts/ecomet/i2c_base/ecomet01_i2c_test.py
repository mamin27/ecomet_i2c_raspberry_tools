#!/usr/bin/env python3

import sys,os
sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  ecomet import ecomet01, ecomet01_constant
import time
#from hdc1080 import hdc1080

import logging

logging.basicConfig(level=logging.DEBUG,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='ecomet01.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

sens = ecomet01.ECOMET01(busnum = 0)
sens._logger = logging.getLogger('ecomet.ecomet01')
sens._logger.info('Start logging ...')

value = 0x10
while (1):
	data = sens.read_register ( register = 'REG00' )
	time.sleep(5)
	data = sens.read_register ( register = 'REG01' )
	time.sleep(5)
	data = sens.read_register ( register = 'REG02' )
	time.sleep(5)
	data = sens.read_register ( register = 'REG03' )
	time.sleep(5)
	data = sens.read_register ( register = 'REG04' )
	time.sleep(5)
	data = sens.read_register ( register = 'REG01' )
	time.sleep(5)
	data = sens.write_register (register = 'REG02', value = [value])
	time.sleep(5)
	data = sens.write_register (register = 'REG03', value = [0x54,value])
	time.sleep(5)
	data = sens.write_register (register = 'REG04', value = [0x55,0x01,0x02,value])
	value = value + 1
	time.sleep(5)
	if (value > 0xFF):
		value = 0x00
	data = sens.read_register ( register = 'REG_UNI' )
	time.sleep(5)
	data = sens.read_register ( register = 'REG03' )
	time.sleep(5)
