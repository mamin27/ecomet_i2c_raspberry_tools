#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui
from time import sleep
import pickle
import os
import json

base_data = 'ina260.data'
file_data = '/tmp/' + base_data

def child ():
   fd = open(file_data,'wb')
   data = chip1.measure_ui()
   pickle.dump(data, fd,-1)
   fd.close()
   os._exit(0)

buf_voltage_1 = {}
buf_current_1 = {}
buf_voltage_2 = {}
buf_current_2 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x46', time = 0.01, i_unit = 'mA', v_unit = 'V')
chip1 = ina260_ui.INA260_UI(chip = '1#0x47', time = 0.01, i_unit = 'mA', v_unit = 'V')

while True:
   newpid = os.fork()
   if newpid == 0:
      child()
   else:
      ((size_current_1,unit_current_1,buf_current_1),(size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_ui()
      os.waitid(os.P_PID,newpid,os.WEXITED)
      break
fd = open(file_data,'rb')
((size_current_2,unit_current_2,buf_current_2),(size_voltage_2,unit_voltage_2,buf_voltage_2)) = pickle.load(fd)
fd.close()

os.remove(file_data)

arr_current_1 = ()
arr_current_2 = ()
arr_voltage_1 = ()
arr_voltage_2 = ()

arr_current_1 = [value for (key,value) in buf_current_1.items()]
arr_current_2 = [value for (key,value) in buf_current_2.items()]
arr_voltage_1 = [value for (key,value) in buf_voltage_1.items()]
arr_voltage_2 = [value for (key,value) in buf_voltage_2.items()]

data_curr1 = {'current_size_1' : size_current_1,'unit_current_1' : unit_current_1,'arr_current_1' : arr_current_1,}
data_voltage1 = {'voltage_size_1' : size_voltage_1,'unit_voltage_1' : unit_voltage_1,'arr_voltage_1' :arr_voltage_1,}
data_curr2 = {'current_size_2' : size_current_2,'unit_current_2' : unit_current_2,'arr_current_2' : arr_current_2,}
data_voltage2 = {'voltage_size_2' : size_voltage_2,'unit_voltage_2' : unit_voltage_2,'arr_voltage_2' :arr_voltage_2,}

json_curr1 = json.dumps(data_curr1)
json_voltage1 = json.dumps(data_voltage1)
json_curr2 = json.dumps(data_curr2)
json_voltage2 = json.dumps(data_voltage2)

fd = open(file_data,'w')
fd.writelines([json_curr1,'\n'])
fd.writelines([json_voltage1,'\n'])
fd.writelines([json_curr2,'\n'])
fd.writelines([json_voltage2,'\n'])
fd.close()
sleep(3.5)

print (':READ::Measure::{}'.format(base_data))
