# i2c_command
# Author: Marian Minar
# Copyright 2020

import time
from smbus2 import SMBus
from ecomet_i2c_sensors import Platform
from ecomet_i2c_sensors.platform import i2c_platform

plat = i2c_platform.plat_list[Platform.platform_detect()]
if plat == 'H616':
   import OPi.GPIO as rGPIO
else:
   import RPi.GPIO as rGPIO


def eeprom_set_addr(addr,smb,slaveaddr,chip) :
    
    haddr = 0x00 + addr
    hslaveaddr = 0x00 + slaveaddr

    if (chip <= 2) :
        smb.write_byte(hslaveaddr, addr%256)
    elif (chip <= 5) :
        if addr//256 > 0 :
            hslaveaddr = hslaveaddr | addr//256 
        smb.write_byte(hslaveaddr, addr%256)
    elif (chip <= 10) :
        smb.write_byte_data(slaveaddr, addr//256, addr%256)
    else :
        if addr//65535 > 0 :
            hslaveaddr = hslaveaddr | addr//65535
        smb.write_byte_data(hslaveaddr, addr//256, addr%256)

# read by byte mode
def eeprom_read_byte(addr,smb,slaveaddr,chip) :
    
    haddr = 0x00 + addr
    hslaveaddr = 0x00 + slaveaddr
    eeprom_set_addr(addr,smb,slaveaddr,chip)

    if (chip > 2 and chip <= 5) :
       if addr//256 > 0 :
           hslaveaddr = hslaveaddr | addr//256
    elif (chip > 11) :
        if addr//65535 > 0 :
            hslaveaddr = hslaveaddr | addr//65535
        
    return smb.read_byte(hslaveaddr) 

# write by byte mode
def eeprom_write_byte(addr, byte, smb, slaveaddr, writestrobe, chip) :

    haddr = 0x00 + addr
    hslaveaddr = 0x00 + slaveaddr

    if (chip <= 2) :
        data = [byte]
        try:
            if plat != 'H616' and writestrobe :
               rGPIO.output(writestrobe, rGPIO.LOW)
            smb.write_i2c_block_data(hslaveaddr, addr%256, data)
            if plat != 'H616' and writestrobe :
               rGPIO.output(writestrobe, rGPIO.HIGH)
        finally:
            time.sleep(0.015)
    elif (chip > 2 and chip <= 5) :
        data = [byte]
        hslaveaddr = hslaveaddr | addr//256
        try:
            rGPIO.output(writestrobe, rGPIO.LOW)
            smb.write_i2c_block_data(hslaveaddr, addr%256, data)
            rGPIO.output(writestrobe, rGPIO.HIGH)
        finally:
            time.sleep(0.015) # data sheet says 10 msec mac
    elif (chip > 5 and chip <= 10) :
        data = [addr%256,byte]
        try:
            rGPIO.output(writestrobe, rGPIO.LOW)
            smb.write_i2c_block_data(slaveaddr, addr//256, data)
            rGPIO.output(writestrobe, rGPIO.HIGH)
        finally:
            time.sleep(0.015)
    else :
        data = [addr%256,byte]
        hslaveaddr = hslaveaddr | addr//65535
        try:
            rGPIO.output(writestrobe, rGPIO.LOW)
            smb.write_i2c_block_data(hslaveaddr, addr//256, data)
            rGPIO.outpu(writestrobe, rGPIO.HIGH)
        finally:
            time.sleep(0.015)
