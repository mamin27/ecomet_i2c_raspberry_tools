from ecomet_i2c_sensors.ina260 import ina260_constant

class set_measure_0(object):
# set parameters of measure for INA260 chip 0
	_mconst = ina260_constant.register
	AVGC	= _mconst.COUNT_1					# average count
	ISHCT	= _mconst.TIME_332_us				# measure current time
	VBUSCT	= _mconst.TIME_332_us				# measure voltage time
	MODE	= _mconst.INA260_MODE_CONTINUOUS	# measure mode

class set_measure_1(object):
# set parameters of measure for INA260 chip 0
	_mconst = ina260_constant.register
	AVGC	= _mconst.COUNT_1					# average count
	ISHCT	= _mconst.TIME_332_us				# measure current time
	VBUSCT	= _mconst.TIME_332_us				# measure voltage time
	MODE	= _mconst.INA260_MODE_CONTINUOUS	# measure mode
