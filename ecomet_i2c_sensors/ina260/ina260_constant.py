# Address:

I2CBUS					= 1         # /dev/i2c-1
INA260_ADDRESS			= 0x45      # 8 bit version Command Mode
INA260_ADDRESS1			= 0x40      # 8 bit version Command Mode
INA260_ADDRESS2			= 0x45      # 8 bit version Command Mode

# LED Registers

class register(object):
# registers INA260
	REG_CONFIG			= 0x00	# Configuration register
	REG_CURRENT			= 0x01	# Current measurement register (signed) in mA
	REG_BUSVOLTAGE		= 0x02	# Bus voltage measurement register in mV
	REG_POWER			= 0x03	# Power calculation register in mW
	REG_MASK_ENABLE		= 0x06 	# Interrupt/Alert setting and checking register
	REG_ALERT_LIMIT		= 0x07 	# Alert limit value register
	REG_MANUFACTURER_ID	= 0xFE	# Manufacturer ID Register
	REG_DIE_UID			= 0xFF	# Die ID and Revision Register

# Modes
	MODE_SHUTDOWN			= 0x00 	# SHUTDOWN: Minimize quiescient current and turn off current into the device inputs. Set another mode to exit shutown mode **/
	MODE_SHUNT_CURRENT_TRIG	= 0x01	# Shunt Current, Triggered
	MODE_BUS_VOLTAGE_TRIG	= 0x02	# Bus Voltage, Triggered
	MODE_CUR_VOLT_TRIG		= 0x03 	# TRIGGERED: Trigger a one-shot measurement of current and bus voltage. Set the TRIGGERED mode again to take a new measurement **/
	MODE_SHUNT_CURRENT_CONT	= 0x05
	MODE_BUS_VOLT_CONT		= 0x06
	MODE_CUR_VOLT_CONT		= 0x07	# CONTINUOUS: (Default) Continuously update

# Current or voltage conversion time
	TIME_140_us 	= 0x0	#140 us
	TIME_204_us 	= 0x1	#204 us
	TIME_332_us 	= 0x2	#332 us
	TIME_558_us 	= 0x3	#558 us
	TIME_1_1_ms 	= 0x4	#1.1 ms (default)
	TIME_2_116_ms 	= 0x5	#2.115 ms
	TIME_4_156_ms 	= 0x6	#4.156 ms
	TIME_8_244_ms 	= 0x7	#8.244 ms

# Averaging count
	COUNT_1		= 0x0		# 1(default)
	COUNT_4		= 0x1		# 4
	COUNT_16	= 0x2		# 16
	COUNT_64	= 0x3		# 64
	COUNT_128	= 0x4		# 128
	COUNT_256	= 0x5		# 256
	COUNT_512	= 0x6		# 512
	COUNT_1024	= 0x7		# 1024
