# RPM = 1/<poles> * ( (<edge_number> - 1)/ COUNT * ( 1/<multiplier>) ) * < fan_tachometer > * 60
# internal fan_tachometer = 32768 Hz


#NF-8A PWM (Noctua) https://noctua.at/en/nf-a8-pwm/specification

POLES               = 2   # poles
EDGE                = 5   # edge_number
MULTIPLIER          = 1   # multiplier
FAN_TACH            = 32768   # fan_tachometer
RANGE               = 0b00 # Min 500 RPM
EDGES               = 0b01 # 5 edges, 2 poles, 1 effective tach (default)
