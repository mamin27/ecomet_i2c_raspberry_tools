#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant
from time import sleep
import pickle
import os
import json

base_data = 'ina260.data'
file_data = '/tmp/' + base_data

def child ():
   fd = open(file_data,'wb')
   data = chip1.measure_u()
   pickle.dump(data, fd,-1)
   fd.close()
   os._exit(0)

buf_current_1 = {}
buf_voltage_2 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x46', time = 1, i_unit = 'mA', mode = ina260_constant.register.MODE_SHUNT_CURRENT_CONT, 
                                      avgc = ina260_constant.register.COUNT_1, ishct = ina260_constant.register.TIME_558_us)
chip1 = ina260_ui.INA260_UI(chip = '1#0x47', time = 1, u_unit = 'mV',mode = ina260_constant.register.MODE_BUS_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_1, vbusct = ina260_constant.register.TIME_558_us)
sens0 = ina260.conf_register_list(address = 0x46)
sens1 = ina260.conf_register_list(address = 0x47)
print ('Reg:{}',format(sens0))
print ('Reg:{}',format(sens1))


while True:
   newpid = os.fork()
   if newpid == 0:
      child()
   else:
      ((size_current_1,unit_current_1,buf_current_1)) = chip0.measure_i()
      os.waitid(os.P_PID,newpid,os.WEXITED)
      break
fd = open(file_data,'rb')
((size_voltage_2,unit_voltage_2,buf_voltage_2)) = pickle.load(fd)
fd.close()

os.remove(file_data)

arr_current_1 = ()
arr_voltage_2 = ()

arr_current_1 = [value for (key,value) in buf_current_1.items()]
arr_voltage_2 = [value for (key,value) in buf_voltage_2.items()]

data_curr1 = {'current_size_1' : size_current_1,'unit_current_1' : unit_current_1,'arr_current_1' : arr_current_1,}
data_voltage2 = {'voltage_size_2' : size_voltage_2,'unit_voltage_2' : unit_voltage_2,'arr_voltage_2' :arr_voltage_2,}

json_curr1 = json.dumps(data_curr1)
json_voltage2 = json.dumps(data_voltage2)
fd = open(file_data,'w')
fd.writelines([json_curr1,'\n'])
fd.writelines([json_voltage2,'\n'])
fd.close()
sleep(0.5)

print (':READ::Measure::{}'.format(base_data))
