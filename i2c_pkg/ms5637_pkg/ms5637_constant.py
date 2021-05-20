# Address:

I2CBUS             = 1         # /dev/i2c-1
MS5637_ADDRESS     = 0x76      # 8 bit version


# Operation Pressure Range
# MIN = 300 mbar 
# MAX = 1200 mbar

# Command (only write):
# A programmable over sample ratio (OSR) allows users to tune the speed and resolution for a variety of applications.
# accuracy increasing with higher CONV number, also time of measurement is increasing
# See Delta-Sigma ADC info
# https://training.ti.com/delta-sigma-adcs-overview
#
# OSR = fMOD/fDATA

RESET				= 0x1E
D1_CONV_256			= 0x40	# Convert D1 (OSR=256) digital pressure value
D1_CONV_512			= 0x42	# Convert D1 (OSR=512)
D1_CONV_1024		= 0x44	# Convert D1 (OSR=1024)
D1_CONV_2048		= 0x46	# Convert D1 (OSR=2048)
D1_CONV_4096		= 0x48	# Convert D1 (OSR=4096)
D1_CONV_8192		= 0x4A	# Convert D1 (OSR=8192)
D2_CONV_256			= 0x50	# Convert D2 (OSR=256) digital temperature value
D2_CONV_512			= 0x52	# Convert D2 (OSR=512)
D2_CONV_1024		= 0x54	# Convert D2 (OSR=1024)
D2_CONV_2048		= 0x56	# Convert D2 (OSR=2048)
D2_CONV_4096		= 0x58	# Convert D2 (OSR=4096)
D2_CONV_8192		= 0x5A	# Convert D2 (OSR=8192)

# conversation time  Time for convertion of signal (OSR)
CONV_256_TIME		= 0.54		#in ms
CONV_512_TIME		= 1.06
CONV_1024_TIME		= 2.08
CONV_2048_TIME		= 4.13
CONV_4096_TIME		= 8.22
CONV_8192_TIME		= 16.44

# onle read
#PROM_READ from 0xA0 - 0xAE (2 bytes)
PROM_PRE_SENS		= 0xA2	# Pressure sensitivity SENST1
PROM_PRE_OFFSET		= 0xA4	# Pressure offset OFFT1
PROM_TMP_PRE_SENS	= 0xA6	# Temperature coefficient of pressure sensitivity | TCS
PROM_TMP_PRE_OFFSET	= 0xA8	# Temperature coefficient of pressure offset | TCO
PROM_REF			= 0xAA	# Reference temperatur | TRef
PROM_TMP_COEF		= 0xAC	# Temperature coefficient of the temperature | TEMPSE
# (3 bytes)
ADC_READ			= 0x00	# ADC Read
