#eeprom_write
# Author: Marian Minar
# Copyright 2020

from ecomet_i2c_sensors.eeprom import chip_list
import RPi.GPIO as rGPIO
import time
import sys
import os
from .. import i2c_command

def write_full_from_file (file,smb,slaveaddr,writestrobe,chip) :
    
    try: 
        chip_list.xchip[chip][1]
    except:
        return 3
    
    f = open(file,"r")
    print ("Write EEprom ...")
    datax = list()
    raw_list = list()
    addr = 0
   
    while addr <= chip_list.xchip[chip][1] :

        idx = 0
        try:
          raw_list = f.readline().replace('  ',' ').split(' ')
        except :
          return 2
        addr = raw_list[0]
        datax = raw_list[1:]
        addr = addr.replace(':','')
        addr = '0x' + addr.strip()
        try:
          addr = int(addr,0)
        except :
          return 2

        while idx <= 15 :
            datax[idx] = datax[idx].replace(':','')
            datax[idx] = '0x' + datax[idx].strip()
            data = int(datax[idx],0)
            try:
                i2c_command.eeprom_write_byte(addr,data,smb,slaveaddr,writestrobe,chip_list.xchip[chip][0])
            except IOError:
                return 1

            idx = idx + 1
            addr = addr + 1

    #    print ("{:04x}:  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}"
    #                   .format(addr-16, int(datax[0],0),int(datax[1],0),int(datax[2],0),int(datax[3],0),int(datax[4],0),int(datax[5],0),int(datax[6],0),int(datax[7],0),
    #                   int(datax[8],0),int(datax[9],0),int(datax[10],0),int(datax[11],0),int(datax[12],0),int(datax[13],0),int(datax[14],0),int(datax[15],0)))    

    rGPIO.cleanup()
    f.close()
   
    return 0
    
def split_strg(text):

    # split the text
    words = text.split(':')

    # for each word in the line:
    for word in words:
		#word.strip()

        # print the word
        print(words)

