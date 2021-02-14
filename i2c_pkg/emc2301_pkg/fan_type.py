# RPM = 1/<poles> * ( (<edge_number> - 1)/ COUNT * ( 1/<multiplier>) ) * < fan_tachometer > * 60
# internal fan_tachometer = 32768 Hz


#NF-8A PWM (Noctua) https://noctua.at/en/nf-a8-pwm/specification

POLES               = 2   # poles
EDGE                = 5   # edge_number
MULTIPLIER          = 1   # multiplier
FAN_TACH            = 32768   # fan_tachometer
RANGE               = 0b00 # Min 500 RPM
EDGES               = 0b01 # 5 edges, 2 poles, 1 effective tach (default)


#Universal
#FAN_CONF1
RANGE_500_1			= 0b00
RANGE_1000_2		= 0b01
RANGE_2000_4		= 0b10
RANGE_4000_8		= 0b11

EDGES_3_1POLE_05	= 0b00
EDGES_5_2POLE_1		= 0b01
EDGES_7_3POLE_15	= 0b10
EDGES_9_4POLE_2		= 0b11

UPDATE_100			= 0b000
UPDATE_200			= 0b001
UPDATE_300			= 0b010
UPDATE_400			= 0b011
UPDATE_500			= 0b100
UPDATE_800			= 0b101
UPDATE_1200			= 0b110
UPDATE_1600		    = 0b111

#FAN_CONF2
DER_OPT_NO_DERIVATE		= 0b00
DER_OPT_BESIC_DERIVATE	= 0b01
DER_OPT_STEP_DERIVATE   = 0b10
DER_OPT_BOTH_DERIVATE   = 0b11

ERR_RNG_0RPM		= 0b00
ERR_RNG_50RPM		= 0b01
ERR_RNG_100RPM		= 0b10
ERR_RNG_200RPM		= 0b11

