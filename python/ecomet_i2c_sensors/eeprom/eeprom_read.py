#eeprom_read
# Author: Marian Minar
# Copyright 2020

from ecomet_i2c_sensors.eeprom import chip_list
import RPi.GPIO as rGPIO 
import time
import sys
import os
from .. import i2c_command

def read_full_to_file (file,smb,slaveaddr,writestrobe,chip) :
    
    try: 
        chip_list.xchip[chip][1]
    except:
        return 2
        
    f = open(file,"w+")
    print ("Read EEprom ...")
    
    for addr in range (0,chip_list.xchip[chip][1],16):

        idx = 0
        datax = list()
        while idx <= 15:
            try:
                data = i2c_command.eeprom_read_byte(addr,smb,slaveaddr,chip_list.xchip[chip][0])
            except IOError:
                return 1
            datax.append(data)
            idx = idx + 1
            addr = addr + 1

        f.write("{:04x}:  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}\n".format((addr-16),datax[0],datax[1],datax[2],datax[3],datax[4],datax[5],datax[6],datax[7],
                                                                                                                                                       datax[8],datax[9],datax[10],datax[11],datax[12],datax[13],datax[14],datax[15]))
    

    rGPIO.cleanup()
    f.close()
        
    return 0
