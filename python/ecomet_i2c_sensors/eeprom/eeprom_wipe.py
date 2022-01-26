# eeprom_wipe.py package
# Author: Marian Minar
# Copyright 2020

from ecomet_i2c_sensors.eeprom import chip_list
import RPi.GPIO as rGPIO 
import time
import sys
import os
from .. import i2c_command


def wipe (smb,slaveaddr,writestrobe,chip) :
    
    try: 
        chip_list.xchip[chip][1]
    except:
        return 2

    print ('Wiping ...')
    
    for addr in range (0,chip_list.xchip[chip][1],16):

        idx = 0
        datax = list() 
        while idx <= 15 :
            data = 0xFF
            datax.append(data)
            try:
                i2c_command.eeprom_write_byte(addr,data,smb,slaveaddr,writestrobe,chip_list.xchip[chip][0])
            except IOError:
                return 1

            idx = idx + 1
            addr = addr + 1
   
      #  print ("{:04x}:  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}"
      #                 .format(addr-16, datax[0],datax[1],datax[2],datax[3],datax[4],datax[5],datax[6],datax[7],
      #                 datax[8],datax[9],datax[10],datax[11],datax[12],datax[13],datax[14],datax[15])) 

    rGPIO.cleanup()
    
    return 0
