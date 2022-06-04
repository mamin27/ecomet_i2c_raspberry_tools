#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant
from time import sleep
import pickle
import os
import json


buf_voltage_1 = {}
buf_current_1 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x44', time = 1, v_unit = 'mV', i_unit = 'mA', mode = ina260_constant.register.MODE_CUR_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_1, vbusct = ina260_constant.register.TIME_558_us, ishct = ina260_constant.register.TIME_558_us)
sens0 = ina260.conf_register_list(address = 0x44)
print ('Reg:{}',format(sens0))

((size_current_1,unit_current_1,buf_current_1),(size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_ui()

arr_current_1 = ()
arr_voltage_1 = ()

arr_current_1 = [value for (key,value) in buf_current_1.items()]
arr_voltage_1 = [value for (key,value) in buf_voltage_1.items()]

data_curr1 = {'current_size_1' : size_current_1,'unit_current_1' : unit_current_1,'arr_current_1' : arr_current_1,}
data_voltage1 = {'voltage_size_1' : size_voltage_1,'unit_voltage_1' : unit_voltage_1,'arr_voltage_1' :arr_voltage_1,}

json_curr1 = json.dumps(data_curr1)
json_voltage1 = json.dumps(data_voltage1)

file = 'ina260.data'
fd = open(file,'w')
fd.writelines([json_curr1,'\n'])
fd.writelines([json_voltage1,'\n'])
fd.close()
sleep(0.5)

print (':READ::Measure1::{}'.format(file))
