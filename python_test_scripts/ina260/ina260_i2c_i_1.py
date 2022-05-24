#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant
from time import sleep
import pickle
import os
import json

buf_current_1 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x44', time = 5, i_unit = 'mA', mode = ina260_constant.register.MODE_SHUNT_CURRENT_CONT, 
                                      avgc = ina260_constant.register.COUNT_4, ishct = ina260_constant.register.TIME_2_116_ms)
sens0 = ina260.conf_register_list(address = 0x44)
print ('Reg:{}',format(sens0))

((size_current_1,unit_current_1,buf_current_1)) = chip0.measure_i()

arr_current_1 = ()

arr_current_1 = [value for (key,value) in buf_current_1.items()]

data_curr1 = {'current_size_1' : size_current_1,'unit_current_1' : unit_current_1,'arr_current_1' : arr_current_1,}

json_curr1 = json.dumps(data_curr1)

file = 'ina260.data'
fd = open(file,'w')
fd.writelines([json_curr1,'\n'])
fd.close()
sleep(3.5)

print (':READ::Measure1::{}'.format(file))
