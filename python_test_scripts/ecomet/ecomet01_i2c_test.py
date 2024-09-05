#!/usr/bin/env python3

import sys,os
sys.path.append(os.getenv("HOME") + '/ecomet_i2c_raspberry_tools/ecomet_i2c_sensors')
from  ecomet import ecomet01, ecomet01_constant

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

sens = ecomet01.ECOMET01()
sens._logger = logging.getLogger('ecomet.ecomet01')
sens._logger.info('Start logging ...')

data = sens.read_register ( register = 'READ2' )

sens._logger.info('Read Reg: (%s)', data)
