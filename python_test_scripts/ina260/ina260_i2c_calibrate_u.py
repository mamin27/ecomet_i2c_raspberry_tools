#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

buf_voltage_1 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x47', time = 0.2, u_unit = 'mV', mode = ina260_constant.register.MODE_BUS_VOLT_CONT, 
                                      avgc = ina260_constant.register.COUNT_4, vbusct = ina260_constant.register.TIME_204_us)

((size_voltage_1,unit_voltage_1,buf_voltage_1)) = chip0.measure_u()

avrg = 0
for key, value in buf_voltage_1.items():
	avrg = avrg + value

final = round(avrg/size_voltage_1,3)
print (':READ::Calibrate::i1::{}::{}'.format(unit_voltage_1,final))

