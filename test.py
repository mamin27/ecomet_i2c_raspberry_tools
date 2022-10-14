from ecomet_i2c_sensors.ina260 import ina260, ina260_ui, ina260_constant

buf = {}
sens0 = ina260.INA260(address = 0x40)
(size,unit,buf) = sens0.measure_current(stime=0.1,unit='mA')
print ('Size: ',format(size))
print ('Units: ', format(unit))
print ('Values: ', format(buf))
