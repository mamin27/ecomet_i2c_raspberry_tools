# Address:
TSL2591_ADDRESS    = 0x29   # 8 bit version

# Registers
ENABLE             = 0x00   # Enable Register
CONTROL            = 0x01   # Control Register
STATUS             = 0x13   # Status Register

							# ALS Register
THR_AI_LTL         = 0x04   # ALS low threshold lower byte Register
THR_AI_LTH         = 0x05   # ALS low threshold upper byte Register
THR_AI_HTL         = 0x06   # ALS high threshold lower byte Register
THR_AI_HTH         = 0x07   # ALS high threshold upper byte Register

							# No Persist ALS Register
THR_NPAI_LTL        = 0x08   # No Persist ALS low threshold lower byte Register
THR_NPAI_LTH        = 0x09   # No Persist ALS low threshold upper byte Register
THR_NPAI_HTL        = 0x0a   # No Persist ALS high threshold lower byte Register
THR_NPAI_HTH        = 0x0b   # No Persist ALS high threshold upper byte Register

							# IC's INFO
PERSIST_FILTER     = 0x0c   # Interrupt persistence filter
PACKAGE_PID        = 0x11   # Pakcage Identification
DEVICE_ID          = 0x12   # Device Identification
DEVICE_STATUS      = 0x13   # Internal Status

							# CHAN#0
CHAN0_L            = 0x14   # CHAN#0 low
CHAN0_H            = 0x15   # CHAN#0 high
							# CHAN#1
CHAN1_L            = 0x16   # CHAN#1 low
CHAN1_H            = 0x17   # CHAN#1 high

# Integration Timing Bits:        

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
DISABLE_POWER	   = 0xfe   # Flag for ENABLE register to disable internal oscillator

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
LUX_DF			   = 762.0
MAX_COUNT_100MS	   = (36863)
MAX_COUNT		   = (65535)
