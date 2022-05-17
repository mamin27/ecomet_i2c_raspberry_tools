# Address:

I2CBUS					= 1         # /dev/i2c-1
ISL28022_ADDRESS		= 0x40      # 8 bit version Command Mode
#INA260_ADDRESS1			= 0x40      # 8 bit version Command Mode
#INA260_ADDRESS2			= 0x45      # 8 bit version Command Mode

# LED Registers

class register(object):
# registers ISL28022
	REG_CONFIG				 = 0x00	# Power-on reset, bus and shunt ranges, ADC acquisition times, mode configuration
	REG_SHUNT_VOLTAGE   	 = 0x01	# Shunt voltage measurement value
	REG_BUS_VOLTAGE			 = 0x02	# Bus voltage measurement value
	REG_POWER				 = 0x03	# Power measurement value
	REG_CURRENT				 = 0x04 # Current measurement value
	REG_CALIBRATION_REG		 = 0x05 # Register used to enable current and power measurements.
	REG_SHUNT_VOLTAGE_THRESH = 0x06	# Min/Max shunt thresholds
	REG_BUS_VOLTAGE_THRESH   = 0x07	# Min/Max VBUS thresholds
	REG_DCS_INTERRUPT_STATUS = 0x08 # Threshold interrupts
	REG_AUX_CONTROL          = 0x09 # Register to control the interrupts and external clock functionality

# Modes
	MODE_POWER_DOWN			= 0x00 	# Power-down
	MODE_SHUNTV_TRIGG		= 0x01 	# Shunt voltage, triggered
	MODE_BUSV_TRIGG			= 0x02	# Bus voltage, triggered
	MODE_SHUNT_BUSV_TRIGG	= 0x03	# Shunt and bus, triggered
	MODE_ADC_OFF			= 0x04	# ADC off (disabled)
	MODE_SHUNTV_CONT		= 0x05	# Shunt Voltage, continuous
	MODE_BUSV_CONT			= 0x06	# Bus voltage, continuous
	MODE_SHUNT_BUSV_CONT	= 0x07	# Shunt and bus, continuous

# BRNG
	BRNG_16V				= 0x00	# BUS_VOLTAGE SCALE RANGE 0..16V
	BRNG_32V				= 0x01	# 0..32V
	BRNG_60V				= 0x02 

# ADC
	ADC_1_12				= 0x00  # from 72us ... 64.01 ms
	ADC_1_13				= 0x01
	ADC_1_14				= 0x02
	ADC_1_15				= 0x03
	ADC_2_15				= 0x09
	ADC_4_15				= 0x0a
	ADC_8_15				= 0x0b
	ADC_16_15				= 0x0c
	ADC_32_15				= 0x0d
	ADC_64_15				= 0x0e
	ADC_128_15				= 0x0f

# PG
	PG_40mV					= 0x00	# GAIN 1 +- 40mV
	PG_80mV					= 0x01	# GAIN 2 +- 80mV
	PG_160mV				= 0x02	# GAIN 4 +- 160mV
	PG_320mV				= 0x03	# GAIN 8 +- 320mV
