#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260	import ina260

try:
  inaA = ina260.INA260(address=0x40,busnum=1)
  chip0 = inaA.self_test()
  
  if not chip0 == 0 :
    statA = 'NOK'
  else :
    statA = 'OK'
  
except:
  statA = 'NCON'
try:  
  inaB = ina260.INA260(address=0x46,busnum=1)
  chip1 = inaB.self_test()
  
  if not chip1 == 0 :
    statB = 'NOK'
  else :
    statB = 'OK'
  
except:
  statB = 'NCON'

print (':TEST::Address::#A:{}::#B:{}'.format(statA,statB))
