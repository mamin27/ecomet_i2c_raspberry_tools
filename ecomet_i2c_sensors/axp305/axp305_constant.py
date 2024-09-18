from ctypes import c_uint8, BigEndianStructure, Union

# Address:
AXP209_ADDRESS     = 0x34   # 8 bit version

# from CHIP battery.sh script
POWER_INPUT_STATUS_REG 				= 0x00
POWER_OPERATING_MODE_REG 			= 0x01
CHARGE_CONTROL_REG 					= 0x33
CHARGE_CONTROL2_REG 				= 0x34
ADC_ENABLE1_REG 					= 0x82
ADC_ENABLE2_REG						= 0x83
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

class ADC_ENABLE1_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("battery_voltage_adc_enable", c_uint8, 1),
            ("battery_current_adc_enable", c_uint8, 1),
            ("acin_voltage_adc_enable", c_uint8, 1),
            ("acin_current_adc_enable", c_uint8, 1),
            ("vbus_voltage_adc_enable", c_uint8, 1),
            ("vbus_current_adc_enable", c_uint8, 1),
            ("aps_voltage_adc_enable", c_uint8, 1),
            ("ts_pin_adc_function_enable", c_uint8, 1),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)

class ADC_ENABLE2_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("apx209_internal_temperature_monitoring_adc_enable", c_uint8, 1),
            ("_reserved_", c_uint8, 3),
            ("gpio0_adc_function_enable", c_uint8, 1),
            ("gpio1_adc_function_enable", c_uint8, 1),
            ("_reserved_", c_uint8, 2),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
