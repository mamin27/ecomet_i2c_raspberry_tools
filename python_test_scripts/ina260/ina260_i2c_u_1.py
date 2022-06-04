#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant
from time import sleep
import pickle
import os
import json

buf_voltage_1 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x44', time = 1, u_unit = 'mV', mode = ina260_constant.register.MODE_BUS_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_4, vbusct = ina260_constant.register.TIME_204_us)
sens0 = ina260.conf_register_list(address = 0x44)
print ('Reg:{}',format(sens0))

((size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_u()

arr_voltage_1 = ()

arr_voltage_1 = [value for (key,value) in buf_voltage_1.items()]

data_voltage1 = {'voltage_size_1' : size_voltage_1,'unit_voltage_1' : unit_voltage_1,'arr_voltage_1' :arr_voltage_1,}

json_voltage1 = json.dumps(data_voltage1)

file = 'ina260.data'
fd = open(file,'w')
fd.writelines([json_voltage1,'\n'])
fd.close()
sleep(3.5)

print (':READ::Measure1::{}'.format(file))
