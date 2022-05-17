#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui
from time import sleep
import pickle
import os
import json

sens = ina260.INA260()

def child ():
   fd = open('ina_chip','wb')
   data = chip1.measure_ui()
   pickle.dump(data, fd,-1)
   fd.close()
   os._exit(0)

buf_current_1 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x45', time = 0.1, i_unit = 'mA', v_unit = 'V')

((size_current_1,unit_current_1,buf_current_1),(size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_ui()

arr_current_1 = ()

arr_current_1 = [value for (key,value) in buf_current_1.items()]

data_curr1 = {'current_size_1' : size_current_1,'unit_current_1' : unit_current_1,'arr_current_1' : arr_current_1,}

json_curr1 = json.dumps(data_curr1)
file = 'ina260.data'
fd = open(file,'w')
fd.writelines([json_curr1,'\n'])
print (':READ::Measure::{}'.format(file))

