#!/usr/bin/env python3

import sys
print (sys.version)
from  i2c_pkg.pca9557_pkg import pca9557
import logging

sens = pca9557.PCA9557()

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='pca9557.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
sens._logger = logging.getLogger('ecomet.pca9557')
sens._logger.info('Start logging ...')

sens.sw_reset()

#sens.write_register(register = 'REGISTER3', value = 60)
sens.set_io('OOIIIIOO')
interrupt = sens.read_input_port(thr = '->0', mtime = 5, offset = 0.01)
if ( interrupt[1] == 0 ) : 
   sens._logger.info('Input signal detected: {}'.format(interrupt[0]))
else :
   sens._logger.info('No Input signal, threshold time reached')
   exit ()

#R0 = sens.read_register('REGISTER0')[0]
#R1 = sens.read_register('REGISTER1')[0]
#R2 = sens.read_register('REGISTER2')[0]
#R3 = sens.read_register('REGISTER3')[0]

#sens.write_register(register = 'REGISTER2', value = 240)
#R2 = sens.read_register('REGISTER2')[0]
#sens.write_register(register = 'REGISTER1', value = 0)
#R1 = sens.read_register('REGISTER1')[0]
#print ("R0 = {}".format(R0))
#print ("R1 = {}".format(R1))
#print ("R2 = {}".format(R2))
#print ("R3 = {}".format(R3))

#sens.read_port()

sens.write_register(register = 'REGISTER1', value = 3)
