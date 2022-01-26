#eeprom_check.py
# Author: Marian Minar
# Copyright 2020

# used for comparing two files for testing writing and reading eeprom

from ecomet_i2c_sensors.eeprom import chip_list
import RPi.GPIO as rGPIO 
from random import randrange
import time
import sys
import os
from .. import i2c_command

def filecmp (file1,file2,smb,slaveaddr,writestrobe,chip) :
    
    try: 
        chip_list.xchip[chip][1]
    except:
        return 3
    
    f = open(file1,"w+")
    print ("Write ...")

    for addr in range (0,chip_list.xchip[chip][1],16):

        idx = 0
        datax = list() 
        while idx <= 15 :
            data = randrange(256)
            datax.append(data)
            try:
                i2c_command.eeprom_write_byte(addr,data,smb,slaveaddr,writestrobe,chip_list.xchip[chip][0])
            except IOError:
                return 1

            idx = idx + 1
            addr = addr + 1

        f.write("{:04x}: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}\n"
        .format((addr-8),datax[0],datax[1],datax[2],datax[3],datax[4],datax[5],datax[6],datax[7],datax[8],datax[9],datax[10],datax[11],datax[12],datax[13],datax[14],datax[15]))
    

    rGPIO.cleanup()
    f.close()
   
    f = open(file2,"w+")
    print ("Read ...")

    for addr in range (0,chip_list.xchip[chip][1],16):

        idx = 0
        datax = list() 
        while idx <= 15:
            try:
                data = i2c_command.eeprom_read_byte(addr,smb,slaveaddr,chip_list.xchip[chip][0])
            except IOError:
                return 2
            datax.append(data)
            idx = idx + 1
            addr = addr + 1

        f.write("{:04x}: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}\n"
        .format((addr-8),datax[0],datax[1],datax[2],datax[3],datax[4],datax[5],datax[6],datax[7],datax[8],datax[9],datax[10],datax[11],datax[12],datax[13],datax[14],datax[15]))
    

    rGPIO.cleanup()
    f.close()
    
    with open(file1,"r") as cmp1:
        with open(file2,"r") as cmp2:
            line1 = cmp1.readlines()
            line2 = cmp2.readlines()
            if line1 != line2 :
                return 4
        cmp2.close()
    cmp1.close()

    os.remove(file1)
    os.remove(file2)
        
    return 0
