from ctypes import c_uint8, BigEndianStructure, Union

# Address:
AS3935_I2C_ADDR3 		= 0x03


# Registers:
POWER_REG				= 0x00
STAT_REG_1				= 0x01
STAT_REG_2				= 0x02
STAT_REG_3				= 0x03
ENG_LIGHT_LB			= 0x04
ENG_LIGHT_HB			= 0x05
ENG_LIGHT_MMSB			= 0x06
DISTANCE_REG			= 0x07					# Distance Register
SET_IRQ_SIGNAL			= 0x08
PRESET_DEFAULT  		= 0x3c
CALIB_RCO				= 0x3d					# Calibrates automatically the internal RC Oscillators

class POWER_REG_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("_reserved_", c_uint8, 2),
            ("afe_gb", c_uint8, 5),  			# AFE Gain Boost Default: 10010
            ("power", c_uint8, 1), 				# 0 Active, 1 Power Down, Power down is OFF at I2C
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    power_up = 0
    power_down = 1

class STAT_REG_1_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("_reserved_", c_uint8, 1),
            ("nf_lev", c_uint8, 3),				# Noise Floor Level
            ("wdth", c_uint8, 4),				# Watchdog threshold
        ]
    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    nfl_in_0 = 0b000							# Indoor 28 uVrms
    nfl_in_1 = 0b001							# Indoor 45 uVrms
    nfl_in_2 = 0b010							# Indoor 62 uVrms
    nfl_in_3 = 0b011							# Indoor 78 uVrms
    nfl_in_4 = 0b100							# Indoor 95 uVrms
    nfl_in_5 = 0b101							# Indoor 112 uVrms
    nfl_in_6 = 0b110							# Indoor 130 uVrms
    nfl_in_7 = 0b111							# Indoor 146 uVrms
    nfl_out_0 = 0b000							# Outdoor 390 uVrms
    nfl_out_1 = 0b001							# Outdoor 630 uVrms
    nfl_out_2 = 0b010							# Outdoor 860 uVrms
    nfl_out_3 = 0b011							# Outdoor 1100 uVrms
    nfl_out_4 = 0b100							# Outdoor 1140 uVrms
    nfl_out_5 = 0b101							# Outdoor 1570 uVrms
    nfl_out_6 = 0b110							# Outdoor 1800 uVrms
    nfl_out_7 = 0b111							# Outdoor 2000 uVrms
    wdth_0    = 0b0000							# WatchDog Threshold Level
    wdth_1	  = 0b0001
    wdth_2    = 0b0010
    wdth_3	  = 0b0011
    wdth_4    = 0b0100
    wdth_5	  = 0b0101
    wdth_6    = 0b0110
    wdth_7	  = 0b0111
    wdth_8    = 0b1000
    wdth_9	  = 0b1001
    wdth_10   = 0b1010

class STAT_REG_2_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("_reserved_", c_uint8, 1),
            ("cl_stat", c_uint8, 1),			# Clear Statistics
            ("min_num_light", c_uint8, 2),		# Minimum Number of Lightning
            ("srej", c_uint8, 4),				# Spike rejection
        ]
    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    stat_high = 1
    stat_low  = 0
    min_num_light_0 = 0b00
    min_num_light_1 = 0b01
    min_num_light_2 = 0b10
    min_num_light_3 = 0b11
    srej_0    = 0b0000							# Spike Rejection Level
    srej_1	  = 0b0001
    srej_2    = 0b0010
    srej_3	  = 0b0011
    srej_4    = 0b0100
    srej_5	  = 0b0101
    srej_6    = 0b0110
    srej_7	  = 0b0111
    srej_8    = 0b1000
    srej_9	  = 0b1001
    srej_10   = 0b1010
    srej_11	  = 0b1011
    srej_12   = 0b1100
    srej_13	  = 0b1101
    srej_14   = 0b1110
    srej_15	  = 0b1111

class STAT_REG_3_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("lco_fdiv", c_uint8, 2),			# Frequency division ration for antenna tunning
            ("mask_dist", c_uint8, 1),			# Mask Disturber, Enable = 0, Disable = 1
            ("_reserved_", c_uint8, 1),
            ("int", c_uint8, 4),  				# Interrupt
        ]
    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    int_nh = 0b0001								# Interrupt Noise level too high
    int_d  = 0b0100								# Disturber detected
    int_l  = 0b1000  							# Lightning interrupt

class ENG_LIGHT_MMSB_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("_reserved_", c_uint8, 3),
            ("s_lig_mm", c_uint8, 5),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)

class ENG_LIGHT_HB_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("s_lig_hb", c_uint8, 8),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)

class ENG_LIGHT_LB_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("s_lig_lb", c_uint8, 8),
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)

class DISTANCE_REG_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [
            ("_reserved_", c_uint8, 2),
            ("distance", c_uint8, 6),  			# Distance Estimation
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    dist_out = 0b111111								# Out of range

class SET_IRQ_SIGNAL_FLAGS(Union):
    class _b(BigEndianStructure):
        _fields_ = [      
            ("disp_lco", c_uint8, 1),				# display lco on IRQ pin
            ("disp_srco", c_uint8, 1),				# display srco on IRQ pin
            ("disp_trco", c_uint8, 1),				# display trco on IRQ pin
            ("_reserved_", c_uint8, 1),
            ("tun_cap", c_uint8, 4) 				# Internal Tunning Capacitors ( from 0 to 120 pf in step 8pf)
        ]

    _fields_ = [("_b", _b),
                ("asbyte", c_uint8)]

    _anonymous_ = ("_b",)
    irq_trco = 1
    irq_srco = 2
    irq_lco = 3

# PRESET_DEFAULT_FLAGS CMD:
class PRESET_DEFAULT_FLAGS(Union):
    reset_cmd = 0x96

# PRESET_DEFAULT_FLAGS CMD:
class CALIB_RCO_FLAGS(Union):
    calib_cmd = 0x96
