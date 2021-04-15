# Address:
I2CBUS             = 1         # /dev/i2c-1
PCA9632_ADDRESS    = 0x62      # 8 bit version 0x62 pca9632
PCA9632_SWRESET    = 0x06      # Software reset add 0xA5 & 0x5A bytes
PCA9632_LEDALLCALL = 0x70      # LED ALL CALL address

PCA9632_SUBADR1    = 0x71
PCA9632_SUBADR2    = 0x72
PCA9632_SUBADR3    = 0x74

# Register

MODE1              = 0x00
MODE2              = 0x01
PWM0               = 0x02
PWM1               = 0x03
PWM2               = 0x04
PWM3               = 0x05
GRPPWM             = 0x06
GRPFREQ            = 0x07
LEDOUT             = 0x08
SUBADR1            = 0x09   # used as subaddress, when MOD1 SUB1 (1)
SUBADR2            = 0x0A   # used as subaddress, when MOD1 SUB2 (1)
SUBADR3            = 0x0B   # used as subaddress, when MOD1 SUB3 (1)
ALLCALLADR         = 0x0C

NO_INCREMENT       = 0x0    # is used when the same register must be accessed several times during a single I2C-bus communication
SEQ_ACCESS         = 0x4    # is used when all the registers must be sequentially accessed
LED_PROG           = 0x5    # is used when the four LED drivers must be individually programmed with different values during the same I2C-bus communication
LED_GLOBAL         = 0x6    # is used when the LED drivers must be globally programmed with different settings during the same I2C-bus communication
GLOBAL_ALL         = 0x7    # is used when individual and global changes must be performed during the same I2C-bus communication

# MODE 1 Bits allow:        

SLEEP              = 0x10   # normal/osciloscop_off
SUB1               = 0x08   # allow/disable SUBADDR1
SUB2               = 0x04   # allow/disable SUBADDR2
SUB3               = 0x02   # allow/disable SUBADDR3
ALLCALL            = 0x01   # does_not/respond to ALLCALL_I2C address

# MODE 1 Bits disable:

SLEEP_N            = 0x0F
SUB1_N             = 0x17
SUB2_N             = 0x1B
SUB3_N             = 0x1D
ALLCALL_N          = 0x1E

# MODE2 Bits allow:

DMBLNK             = 0x10
DMBLNK_DIMMING     = 0x10
INVRT              = 0x08   # set output parameter
OCH                = 0x04 
OUTDRV             = 0x02   # set output parameter

# MODE2 Bits disable:

DMBLNK_BLINKING    = 0x0F
INVRT_N            = 0x17
OCH_N              = 0x1B
OUTDRV_N           = 0x1D

# DBMLNK Status:
DIMMING			   = 0x00  # 0 - DIMMING
BLINING            = 0x01  # 1 - BLINKING

# LEDOUT Bits:

LDR0               = 0x03
LDR1               = 0x0C
LDR2               = 0x30
LDR3               = 0xC0

# LEDOUT Bits Write:

LDR0_W             = 0xFC
LDR1_W             = 0xF3
LDR2_W             = 0xCF
LDR3_W             = 0x3F 

# LEDOUT Mode:

OFF                = 0x00   # LED driver x is off
ON                 = 0x01   # LED driver x is fully on
PWM                = 0x02   # LED driver x individual brightness can be controlled through its PWMx register.
PWM_GRPPWM         = 0x03   # LED driver x individual brightness and group dimming/blinking can be controlled through its PWMx register and the GRPPWM registers.
