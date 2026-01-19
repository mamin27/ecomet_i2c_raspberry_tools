WINDS_ADDR        = 0x30
# Register

REG_SERIAL_NUMBER  = 0x00	# 4 bytes read register
REG_CONF           = 0x01	# 1 byte read/write register
REG_INIT           = 0x02	# 1 byte read/write register

REG_AVG00          = 0x03	# 2 bytes read register
REG_AVG30          = 0x04	# 3 bytes read register
REG_AVG60          = 0x05   # 3 bytes read register
REG_AVG360         = 0x06   # 3 bytes read register

REG_GUST00         = 0x07   # 2 bytes read register
REG_GUST30         = 0x08   # 2 bytes read register
REG_GUST60         = 0x09   # 2 bytes read register
REG_GUST360        = 0x0A   # 2 bytes read register
REG_ValidCnt       = 0x0B	# 1 byte read register
REG_EE_Index       = 0x0C	# 1 byte read register
REG_BULK           = 0x0D	# 19 bytes read register
REG_EEPROM_AVG     = 0x0E	# 128 bytes read register
REG_EEPROM_GUST    = 0x0F	# 128 bytes read register

VDD = 5		# Voltage = 5V
MAX_DEGREE = 360 # 360 Degree max position
WEST = 75
SOUTH = 176
EAST = 280
NORTH = 360
NORTH_WEST = 36
SOUTH_WEST = 125
SOUTH_EAST = 225
NORTH_EAST = 330

MAX_VDD = 4095

