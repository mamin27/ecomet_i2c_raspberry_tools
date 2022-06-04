from ecomet_i2c_sensors.ina260 import ina260_constant

class set_measure_0(object):
# set parameters of measure for INA260 chip 0
	_mconst = ina260_constant.register
	AVGC	= _mconst.COUNT_1					# average count
	ISHCT	= _mconst.TIME_1_1_ms				# measure current time
	VBUSCT	= _mconst.TIME_1_1_ms				# measure voltage time
	MODE	= _mconst.MODE_SHUNT_CURRENT_CONT	# measure mode

class set_measure_1(object):
# set parameters of measure for INA260 chip 1
	_mconst = ina260_constant.register
	AVGC	= _mconst.COUNT_1					# average count
	ISHCT	= _mconst.TIME_1_1_ms				# measure current time
	VBUSCT	= _mconst.TIME_1_1_ms				# measure voltage time
	MODE	= _mconst.MODE_SHUNT_CURRENT_CONT	# measure mode
