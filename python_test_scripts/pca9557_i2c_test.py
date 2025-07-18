#!/usr/bin/env python3

import sys
print (sys.version)
from  ecomet_i2c_sensors.pca9557 import pca9557
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
sens.set_invert('NNNNNNNN')
sens.set_io_name(port_arr = [[0,'LED1'],[1,'LED2'],[2,'BUT_RIG_DWN'],[3,'BUT_RIG_UP'],
                             [4,'BUT_LFT_DWN'],[5,'BUT_LFT_UP'],[6,'DIS_RST'],[7,'D/C']])
show = sens.port_show_name(setting = 'io')
sens._logger.info('Show Ports:')
for i in range(8) :
   sens._logger.info('PIN{}: {} : {} : {}'.format(i,show[0][i][0],show[0][i][1],show[0][i][2]))


sens._logger.info('Push 10 times any Button ....')
for j in range (1) :
   interrupt = sens.read_input_port(thr = 'Unset', mtime = 6, offset = 0.5)
   if ( interrupt[1] == 0 ) : 
      #sens._logger.info('Input signal detected:')
      for i in range(8) :
         sens._logger.info('PIN{}: {} : {} : {}'.format(i,interrupt[0][i][0],interrupt[0][i][1],interrupt[0][i][2]))
         if ( interrupt[0][i][1] == pca9557.Threshold ) :
             sens._logger.info('Loop:{} -> PIN{}: {} ... pushed'.format(j,interrupt[0][i][0],interrupt[0][i][2])) 
   else :
      sens._logger.info('Loop:{} -> No Input signal, threshold time reached'.format(j))

sens.reset_outputs()
sens.port_display()


sens.write_output_port (status = pca9557.Low, pin = 'LED1')
sens.write_output_port (status = pca9557.High, pin = 'LED2')
sens.port_display()

from time import sleep
sleep(5)
sens.write_output_port (status = pca9557.High, pin = 'LED1')
sens.write_output_port (status = pca9557.Low, pin = 'LED2')
sens.port_display()

sleep(5)
sens.write_output_port (status = pca9557.High, pin = 'LED1')
sens.write_output_port (status = pca9557.High, pin = 'LED2')
sens.port_display()

R0 = sens.read_register('REGISTER0')[0]
R1 = sens.read_register('REGISTER1')[0]
R2 = sens.read_register('REGISTER2')[0]
R3 = sens.read_register('REGISTER3')[0]

#sens.write_register(register = 'REGISTER2', value = 240)
#R2 = sens.read_register('REGISTER2')[0]
#sens.write_register(register = 'REGISTER1', value = 0)
#R1 = sens.read_register('REGISTER1')[0]
print ("R0 = {}".format(R0))
print ("R1 = {}".format(R1))
print ("R2 = {}".format(R2))
print ("R3 = {}".format(R3))

