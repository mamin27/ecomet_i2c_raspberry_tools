#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant
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

buf_voltage_1 = {}
buf_current_1 = {}
buf_voltage_2 = {}
buf_current_2 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x44', time = 1, v_unit = 'mV', i_unit = 'mA', mode = ina260_constant.register.MODE_CUR_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_1, vbusct = ina260_constant.register.TIME_1_1_ms, ishct = ina260_constant.register.TIME_1_1_ms)
chip1 = ina260_ui.INA260_UI(chip = '1#0x45', time = 1, v_unit = 'mV', i_unit = 'mA', mode = ina260_constant.register.MODE_CUR_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_1, vbusct = ina260_constant.register.TIME_1_1_ms, ishct = ina260_constant.register.TIME_1_1_ms)
sens0 = ina260.conf_register_list(address = 0x44)
sens1 = ina260.conf_register_list(address = 0x45)
print ('Reg:{}',format(sens0))
print ('Reg:{}',format(sens1))


while True:
   newpid = os.fork()
   if newpid == 0:
      child()
   else:
      ((size_current_1,unit_current_1,buf_current_1),(size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_ui()
      os.waitid(os.P_PID,newpid,os.WEXITED)
      break
fd = open('ina_chip','rb')
((size_current_2,unit_current_2,buf_current_2),(size_voltage_2,unit_voltage_2,buf_voltage_2)) = pickle.load(fd)
fd.close()
#print('{}'.format(os.listdir()))
os.remove('ina_chip')

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
file = 'ina260.data'
fd = open(file,'w')
fd.writelines([json_curr1,'\n'])
fd.writelines([json_voltage1,'\n'])
fd.writelines([json_curr2,'\n'])
fd.writelines([json_voltage2,'\n'])
fd.close()
sleep(0.5)

print (':READ::Measure::{}'.format(file))