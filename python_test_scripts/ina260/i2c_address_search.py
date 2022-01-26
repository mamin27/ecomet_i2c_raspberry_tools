#!/usr/bin/env python3

from  ecomet_i2c_sensors.platform import i2c_platform

plat = i2c_platform.Board_plat(busnum=1,arange=[0x40,0x4F])
board = plat.board()
bus = plat.bus()
slave = plat.slaves()

if not slave :
  print (':ERROR::No I2C Address found')
else :
    print (':SEARCH::Address::size:{}::address:{}'.format(len(slave.split(':')),slave))

