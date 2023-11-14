from ctypes import c_uint8, BigEndianStructure, Union

# Address:
AXP209_ADDRESS     = 0x34   # 8 bit version

# from CHIP battery.sh script
POWER_INPUT_STATUS_REG 				= 0x00
POWER_OPERATING_MODE_REG 			= 0x01
CHARGE_CONTROL_REG 					= 0x33
CHARGE_CONTROL2_REG 				= 0x34
ADC_ENABLE1_REG 					= 0x82
INTERNAL_TEMPERATURE_REG 			= 0x5e
BATTERY_VOLTAGE_REG 				= 0x78
BATTERY_CHARGE_CURRENT_REG 			= 0x7a
BATTERY_DISCHARGE_CURRENT_REG 		= 0x7c
GPIO0_FEATURE_SET_REG 				= 0x90
GPIO1_FEATURE_SET_REG 				= 0x92
GPIO2_FEATURE_SET_REG 				= 0x93
BATTERY_GAUGE_REG 					= 0xb9
VBUS_IPSOUT_CHANNEL_MANAGEMENT_REG 	= 0X30

# POWER_OPERATING_MODE_REG Bits:
class POWER_OPERATING_STATUS_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("over-temperature", c_uint8, 1), 	# instruct  AXP209 Is it overheated? 0:Not too warm ； 1:Overtemperature
            ("battery_charging", c_uint8, 1),  	# Charging instructions 
												# 0:Not charging or charging completed ； 1:Charging
            ("battery_exists", c_uint8, 1),		# Battery presence status indication 
												# 0:No battery connected to  AXP209； 1:The battery is connected to  AXP209
            ("_reserved_", c_uint8, 1),	
            ("battery_active", c_uint8, 1),		# Indicates whether the battery has entered activation mode 
												# 0:Not entering battery activation mode ； 1:Entered battery activation mode
            ("reached_desired_charge_current", c_uint8, 1),		# Indicates whether the charging current is less than the expected current 
												# 0:The actual charging current is equal to the expected current ； 1:The actual charging current is less than the expected current 
            ("_reserved_", c_uint8, 2),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)

class POWER_INPUT_STATUS_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("acin_present", c_uint8, 1),
            ("acin_available", c_uint8, 1),
            ("vbus_present", c_uint8, 1),
            ("vbus_available", c_uint8, 1),
            ("vbus_direction", c_uint8, 1),
            ("battery_current_direction", c_uint8, 1),  # 1: charging, 0: discharging
            ("acin_vbus_shorted", c_uint8, 1),
            ("start_source", c_uint8, 1)
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)


class POWER_OPERATING_STATUS_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("over-temperature", c_uint8, 1),
            ("battery_charging", c_uint8, 1),  # 1: charging, 0: not charging or charging done
            ("battery_exists", c_uint8, 1), # 1: battery is connected, 0: not connected
            ("_reserved_", c_uint8, 1),
            ("battery_active", c_uint8, 1),
            ("reached_desired_charge_current", c_uint8, 1),
            ("_reserved_", c_uint8, 2),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)


class GPIO012_FEATURE_SET_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("gpio_rising_edge_interupt", c_uint8, 1),
            ("gpio_falling_edge_interupt", c_uint8, 1),
            ("_reserved_", c_uint8, 3),
            ("gpio_function", c_uint8, 3),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)


class VBUS_CURRENT_LIMIT_CONTROL(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("vbus_available", c_uint8, 1),
            ("hold_pressure_limiting", c_uint8, 1),
            ("hold_set_up", c_uint8, 3),
            ("_reserved_", c_uint8, 1),
            ("vbus_current_limit", c_uint8, 2),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    
						    



       

TIME_100MS         = 0x00   # 100 ms
TIME_200MS         = 0x01   # 200 ms
TIME_300MS         = 0x02   # 300 ms
TIME_400MS         = 0x03   # 400 ms
TIME_500MS         = 0x04   # 500 ms
TIME_600MS         = 0x05   # 600 ms


# Enumeration for the persistance filter
PERSIST_EVERY      = 0x00   # Every ALS cycle generates an interrupt
PERSIST_ANY		   = 0x01   # Any value otside of threshold range
PERSIST_2		   = 0x02   # 2 consecutive values out of range
PERSIST_3		   = 0x03   # 3 consecutive values out of range
PERSIST_5		   = 0x04   # 5 consecutive values out of range
PERSIST_10		   = 0x05   # 10 consecutive values out of range
PERSIST_15		   = 0x06   # 15 consecutive values out of range
PERSIST_20		   = 0x07   # 20 consecutive values out of range
PERSIST_25		   = 0x08   # 25 consecutive values out of range
PERSIST_30		   = 0x09   # 30 consecutive values out of range
PERSIST_35		   = 0x0a   # 35 consecutive values out of range
PERSIST_40		   = 0x0b   # 40 consecutive values out of range
PERSIST_45		   = 0x0c   # 45 consecutive values out of range
PERSIST_50		   = 0x0d   # 50 consecutive values out of range
PERSIST_55		   = 0x0e   # 55 consecutive values out of range
PERSIST_60		   = 0x0f   # 60 consecutive values out of range

# Enumeration for the sensor gain
GAIN_LOW           = 0x00  # low gain (1x)
GAIN_MED           = 0x10  # medium gain (25x)
GAIN_HIGH          = 0x20  # medium gain high (428x)
GAIN_MAX           = 0x30  # max gain (9876x)

# LUX coefficient
#LUX_DF             = '408.0F' # Lux coefficient
#LUX_COEFB		   = '1.64F'  # CH0 coefficient
#LUX_COEFC		   = '0.59F'  # CH1 coefficient A
#LUX_COEFD		   = '0.86F'  # CH2 coefficient B

# Commands
COMMAND_BIT		   = 0xa0   # 1010 0000: bits 7 and 5 for 'command normal'
#CLEAR_INT		   = 0xe7   # Special Function Command for "Clear ALS and no persist ALS interrupt"
#TEST_INT		   = 0xe4   # Special Function Command for "Interrupt set - forces an interrupt"
#WORD_BIT		   = 0x20   # < 1 = read/write word (rather than byte)
#LOCK_BIT		   = 0x10   # < 1 = using block read/write

# Enable Mask Bit
ENABLE_NPIEN	   = 0x80   # No Persist Interrupt Enable. When asserted NP Threshold conditions will generate an interrupt, bypassing the persist filter.
ENABLE_SAI		   = 0x20   # Sleep after interrupt. When asserted, the device will power down at the end of an ALS cycle if an interrupt has been generated.
ENABLE_AIEN 	   = 0x10   # ALS Interrupt Enable. When asserted permits ALS interrupts to be generated, subject to the persist filter.
ENABLE_AEN		   = 0x02   # ALS Enable. This field activates ALS function. Writing a one activates the ALS. Writing a zero disables the ALS.
ENABLE_POWER	   = 0x01   # Flag for ENABLE register to enable intrnal oscillator
DISABLE_NPIEN	   = 0x3f
DISABLE_SAI		   = 0x5f
DISABLE_AIEN	   = 0xef
DISABLE_AEN		   = 0xfd
DISABLE_POWER	   = 0x00   # Flag for ENABLE register to disable internal oscillator

# Control Mask Bit
CTLR_RESET		   = 0x80   # System reset. When asserted, the device will reset equivalent to a power-on reset. SRESET is self-clearing.
CTLR_AGAIN		   = 0x30   # ALS gain sets the gain of the internal integration amplifiers for both photodiode channels.
CTLR_ATIME		   = 0x07   # ALS time sets the internal ADC integration time for both photodiode channels.

# Mask Bits
PERSIST			   = 0x0f   # ALS interrupt persistence filter
PID_MASK		   = 0x18   # DEVICE_PID MASK
NPINTR_MASK		   = 0x10   # No-persist Interrupt. Indicates that the device has encountered a no-persist interrupt condition. MASK
AINT_MASK		   = 0x08   # ALS Interrupt. Indicates that the device is asserting an ALS interrupt. MASK
AVALID_MASK		   = 0x01   # ALS Valid. Indicates that the ADC channels have completed an integration cycle since the AEN bit was asserted.

#LUX_DB coeficient
LUX_DF			   = 408.0
LUX_COEFB		   = 1.64
LUX_COEFC		   = 0.59
LUX_COEFD		   = 0.86
MAX_COUNT_100MS	   = (36863)
MAX_COUNT		   = (65535)

#Special Commands
SetInterrupt	     = 0xe4 # Interrupt set  forces an interrupt
ClearAlsInt		     = 0xe6 # Clears ALS interrupt
ClearAlsNoPersAlsInt = 0xe7 # Clears ALS and no persist ALS interrupt
ClearsNoPersAlsInt   = 0xea # Clears no persist ALS interrupt

# The interrupt set special function command sets the interrupt bits 
# in the status register (0x13). For the interrupt to be visible on the 
# INT pin, one of the interrupt enable bits in the enable register 
# (0x00) must be asserted.
# The interrupt set special function must be cleared with an interrupt 
# clear special function. The ALS interrupt clear special functions 
# clear any pending interrupt(s) and are self-clearing.
