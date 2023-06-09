#!/usr/bin/env python3

#eeprom I2c read/write script
#!/usr/bin/python3
# code to eeprom  24c01 - 24c1024 by rasberry pi
# Tested at
# Raspberry pi 3 B+
# AT24C256 IIC EEPROM Memory Module (https://pixelelectric.com/at24c256-iic-eeprom-memory-module/)
# EEPROM CHIPs, 24c04, 24c32, 24c64

# Author: Marian Minar
# Copyright 2020

from colorama import Fore
import sys, getopt
import yaml
from smbus2 import SMBus
import os,re

from ecomet_i2c_sensors import i2c_command,Platform
from ecomet_i2c_sensors.platform import i2c_platform
from ecomet_i2c_sensors.eeprom import chip_list
from ecomet_i2c_sensors.eeprom import eeprom_check
from ecomet_i2c_sensors.eeprom import eeprom_wipe
from ecomet_i2c_sensors.eeprom import eeprom_read
from ecomet_i2c_sensors.eeprom import eeprom_write

plat = i2c_platform.plat_list[Platform.platform_detect()]
if plat == 'H616':
   import OPi.GPIO as rGPIO
else:
   import RPi.GPIO as rGPIO

path = os.path.expanduser('~/.comet')
with open(path + "/config.yaml") as c: 
    try:
        config = yaml.safe_load(c)
    except yaml.YAMLError as exc:
        print(exc)

ic = config['i2c']['eeprom']['ic']
slaveaddr= config['i2c']['eeprom']['slaveaddr'] # for eeprom (main i2c address)
smb = SMBus(int(re.search("^i2c-(\d+)$",config['i2c']['smb']).group(1))) # set bus i2c-1
writestrobe = config['i2c']['eeprom']['writestrobe'] # hold pin low to write to eeprom

rGPIO.setmode(rGPIO.BOARD)
rGPIO.setwarnings(False)
if plat != 'H616':
   rGPIO.setup(writestrobe, rGPIO.OUT)

def help() :
    print ('eeprom_mgr.py <option>')
    print (' option:')
    print ('  -h help')
    print ('  -p chip name')
    print ('  -t run in test mode')
    print ('  -e wipe eeprom')
    print ('  -r read content of chip')
    print ('  -w write into chip')
    print ('  -f file name, used with read and write commands')
    print (' ')
    print (' <-p>,<--chip> chip name:')
    print ('   this attribute default read from ~/.comet/config.yaml')
    print ('   list of these chips are usable')
    print ('   24C01,24C02,24C04,24C08,24C16,24C32,24C64,24C128,24C256,24C512,24C1024')
    print (' <-t>|<--test> test mode:')
    print ('   test mode will write random number into chip, read contentant and compare')
    print (' <-e>|<--wipe> wipe:')
    print ('    wipping data at chip')
    print (' <-r>,<--read> read:')
    print ('   read content of chip and write into file <-f>')
    print (' <-w>,<--write> write:')
    print ('   write content from file <-f> into chip')
    print (' Note: when file attribute is not added will be used default file name')
    #print (' <-m> file mod:')
    #print ('   file could be stored in two mods:')
    #print ('   row - row hexadecimal mode')
    #print ('   wide - explaining hexadecimal mode')


if __name__ == '__main__' :
    
    chip = "n/a"
    test = False
    wipe = False
    read = False
    write = False
    ffile = "data/Dummy"
    
    if len(sys.argv) == 1 :
        help()
        sys.exit(10)

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hp:trwef:",["read","write","test","wipe","chip=","file="])
    except getopt.error:
        help()
        sys.exit(10)
    if ic :
       chip = ic
    for opt, arg in opts:
        if opt == ('-h','--help'):
            help()
            sys.exit()
        elif opt in ('-p','--chip'):
            chip = arg
            chip = chip.lower()
            print ('Chip {}'.format(chip))
        elif opt in ('-e','--wipe'):
            wipe = True
        elif opt in ('-t', '--test'):
            test = True
        elif opt in ('-r', '--read'):
            read = True
        elif opt in ('-w', '--write'):
            write = True
        elif opt in ('-f', '--file'):
            ffile = arg
    mode = rGPIO.getmode();
    version = rGPIO.BOARD

    
    print ("Model: {}".format(mode))
    #print ("Board version: {}".format(version['TYPE']))
    #print ("Board RAM: {}".format(version['RAM']))
    print ("Chip: {}".format(chip))
    print ("I2C Bus: {}".format(config['i2c']['smb']))
    print ("I2C Address: 0x{:02x}".format(config['i2c']['eeprom']['slaveaddr']))
    chip_list.init()

    wfile = "data/eeprom_wr_" + chip + ".hex"
    rfile = "data/eeprom_rd_" + chip + ".hex"
    
    if (ffile == 'data/Dummy'):
        if ( read or write):
            ffile = "data/eeprom_" + chip + ".hex"
        
    
    if (test):
        if ( chip == 'n/a' ) :
            print (Fore.RED + 'Chip is not declared. Test needs chip declaration')
            sys.exit(20)
        print('Check Chip funcionality ...')
        cmp = eeprom_check.filecmp (wfile,rfile,smb,slaveaddr,writestrobe,chip)
        if (cmp == 0) :
            print (Fore.GREEN + 'Chip correctly checked');
            sys.exit(0)
        elif (cmp == 1) :
            print (Fore.RED + 'Error in Chip writting process')
            sys.exit(1)
        elif (cmp == 2) :
            print (Fore.RED + 'Error in Chip reading process')
            sys.exit(2)
        elif (cmp == 3) :
            print (Fore.RED + 'Incorrect chip selected')
            sys.exit(3)
        else: 
            print (Fore.RED + 'Writing and Reading Chip is not same')
            sys.exit(4)
            
    if (wipe) :
        if ( chip == 'n/a' ) :
            print (Fore.RED + 'Chip is not declared. Wipe needs chip declaration')
            sys.exit(20)
        print('Wipe eeprom ...')
        cmp = eeprom_wipe.wipe (smb,slaveaddr,writestrobe,chip)
        if (cmp == 0) :
            print (Fore.GREEN + 'Chip wipped correctly');
            sys.exit(0)
        elif (cmp == 1) :
            print (Fore.RED + 'Incorrect chip wipping')
            sys.exit(1)
        elif (cmp == 2) :
            print (Fore.RED + 'Incorrect chip selected')
            sys.exit(2)
            
    if (read) :
        if ( chip == 'n/a' ) :
            print (Fore.RED + 'Chip is not declared. Read needs chip declaration')
            sys.exit(20)
        print ('Read eeprom ...')
        print ('Data file write into file {} ...'.format(ffile))
        cmp = eeprom_read.read_full_to_file (ffile,smb,slaveaddr,writestrobe,chip)
        if (cmp == 0) :
            print (Fore.GREEN + 'Chip data writed into file correctly')
            sys.exit(0)
        elif (cmp == 1) :
            print (Fore.RED + 'Chip data read incorrectly')
            sys.exit(1)
        elif (cmp == 2) :
            print (Fore.RED + 'Incorrect chip selected')
            sys.exit(2)
  
    if (write) :
        if ( chip == 'n/a' ) :
            print (Fore.RED + 'Chip is not declared. Write needs chip declaration')
            sys.exit(20)
        print ('Writting eeprom ...')
        print ('Data file writting into eeprom, from file {} ...'.format(ffile))
        cmp = eeprom_write.write_full_from_file (ffile,smb,slaveaddr,writestrobe,chip)
        if (cmp == 0) :
            print (Fore.GREEN + 'EEprom writed from file correctly')
            sys.exit(0)
        elif (cmp == 1) :
            print (Fore.RED + 'EEprom writed incorrectly')
            sys.exit(1)
        elif (cmp == 2) :
            print (Fore.RED + 'File with wrong syntax')
            sys.exit(2)
        elif (cmp == 3) :
            print (Fore.RED + 'Incorrect chip selected')
            sys.exit(3)
    
