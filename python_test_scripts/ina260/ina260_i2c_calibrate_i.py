#!/usr/bin/env python3

from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

buf_current_1 = {}

chip0 = ina260_ui.INA260_UI(chip = '0#0x46', time = 0.2, i_unit = 'mA', mode = ina260_constant.register.MODE_SHUNT_CURRENT_CONT, 
                                      avgc = ina260_constant.register.COUNT_4, ishct = ina260_constant.register.TIME_204_us)

((size_current_1,unit_current_1,buf_current_1)) = chip0.measure_i()

avrg = 0
for key, value in buf_current_1.items():
#	print ('{}'.format(value))
	avrg = avrg + value

final = round(avrg/size_current_1,2)
print (':READ::Calibrate::i1::{}::{}'.format(unit_current_1,final))

